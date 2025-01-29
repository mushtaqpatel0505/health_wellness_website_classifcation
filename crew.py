from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import ScrapeWebsiteTool
from crewai_tools import ScrapeElementFromWebsiteTool
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
load_dotenv()

# Define structured output with three separate lists
class WebsiteEvaluationResults(BaseModel):
    websites: List[str]
    health_wellness: List[bool]
    reasons: List[str]

deepseek_llm = LLM(
    model="deepseek/deepseek-chat",   #"deepseek/deepseek-reasoner",
    api_key="sk-9197a124886146319066fce372d420c5",#"sk-0b46992bab244d5aafc00f3815ef18fb",
    base_url="https://api.deepseek.com/v1"
)
#sk-9197a124886146319066fce372d420c5
@CrewBase
class HealthAndWellnessWebsiteContentAnalysisProcessCrew():
    """HealthAndWellnessWebsiteContentAnalysisProcess crew"""

    @agent
    def website_content_scraper(self) -> Agent:
        return Agent(
            config=self.agents_config['website_content_scraper'],
            tools=[ScrapeWebsiteTool()],
            #llm=deepseek_llm,
            max_iter = 2,
            max_execution_time = 5,
            verbose = False,
            system_message=  "you are an website content scrapper assistant. Scrape the main content of the provided list of URLs Scrape the main content of the websites from the provided list of URLs to analyze their focus on health and wellness. your backstory - As a specialized Website Content Scraper, you excel at extracting relevant information from websites quickly and accurately. Your goal is to gather only the main content, avoiding peripheral pages, to assess the site's relevance to health and wellness. Process all URLs in a single batch and return results in the same order."
        )

    @agent
    def health_and_wellness_content_evaluator(self) -> Agent:
        return Agent(
            config=self.agents_config['health_and_wellness_content_evaluator'],
            tools=[ScrapeElementFromWebsiteTool()],
            #llm=deepseek_llm,
            max_iter = 1,
            max_execution_time = 3,
            verbose=False,
            system_message= "you are an health and wellness content evaluator assitant. Evaluate the scraped content for all URLs in the provided batch to determine if each website belongs to the health and wellness category. Return results in the same order as the input.Evaluate the scraped content against the defined Health and Wellness criteria to determine if the each website belongs in this category. your backstory: With expertise in health and wellness, you analyze website content to categorize it based on specific criteria that reflect direct health services, environmental health, and wellness products and services."
        )


    @task
    def scrape_website_content_task(self) -> Task:
        return Task(
            config=self.tasks_config['scrape_website_content_task'],
            tools=[ScrapeWebsiteTool()],
        )

    @task
    def evaluate_content_for_health_and_wellness_task(self) -> Task:
        return Task(
            config=self.tasks_config['evaluate_content_for_health_and_wellness_task'],
            tools=[ScrapeElementFromWebsiteTool()],
            output_pydantic=WebsiteEvaluationResults,)
        

    # @task
    # def generate_final_boolean_list_task(self) -> Task:
    #     return Task(
    #         config=self.tasks_config['generate_final_boolean_list_task'],
            
    #     )


    @crew
    def crew(self) -> Crew:
        """Creates the HealthAndWellnessWebsiteContentAnalysisProcess crew"""
        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=False,
        )
