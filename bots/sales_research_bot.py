import os
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import SystemMessagePromptTemplate, PromptTemplate
from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain import hub
from langchain.tools import Tool

import requests
from dotenv import load_dotenv
load_dotenv()

MODEL = 'gpt-4o'
PROMPT= """
# Comprehensive Account Plan

## Objective
As a senior research analyst at Gartner, create a detailed account plan for the business specified in the provided URL.

## Process
For each section, use the specified tools and follow the guidelines to gather and present information.

## Sections

1. Business Model
   - Provide a summary explaining how the business operates and generates revenue.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

2. Product Portfolio
   - List key products and services, each with a single sentence description.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

3. Sales Channels
   - Enumerate the publicly available sales channels.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

4. Company Financials
   - List key financial metrics:
     - Current year and past years sales
     - Profit
     - Funding raised (if applicable)
     - Share price (if publicly traded)
   - Use `tavily_search_tool` to analyze websites.
   - Cite all references and source links.

5. Customer Support
   - Identify the main customer support channels, each with a single sentence description.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

6. Sustainability Initiatives
   - List the company's sustainability initiatives, each with a single sentence description.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

7. Recent News Articles and Events
   - Summarize recent news articles and events related to the company.
   - Use `tavily_search_tool` for information.
   - Cite all references and source links.

8. Key Personnel
   For each of the following positions:
   - Chief Executive Officer
   - Chief Financial Officer
   - Chief Operating Officer
   - Chief Technology Officer
   - Chief Information Officer
   - Chief Marketing Officer
   - Head of Sales
   - Head of Business Development
   - Consulting Director
   - Human Resources Director
   - Accounting Director
   - Legal Director
   - Engineering Director

   Execute the following steps:
      a. Use tavily_search_tool to find:

      First Name
      Last Name
      Organization Name
      Organization Domain

      b. Use apollo_io_people_enrichment with the information from step a to retrieve:

      Contact Details
      Work History
      Education
      Skills
      Social Media Profiles
      Any other relevant professional information
      Cite all references and source links.

   - Cite all references and source links.

9. Key Openings
   - List at least 5 names and titles of currently open job roles.
   - Provide a single-line summary of the job description for each opening.
   - Search online job boards for the company name using `tavily_search_tool`.
   - Cite all references and source links.

10. AI (Artificial Intelligence) Strategy
    - Provide a detailed summary of the company's AI strategy.
    - Focus only on information pertaining to the AI strategy of the specified company.
    - Use `tavily_search_tool` for information.
    - Cite all references and source links.

11. Apollo.io Enrichment
    Use the `apollo_io_organization_enrichment` tool to get:
    - Total Number of Employees
    - Departmental headcount
    - Industry
    - Social Media Links
    - Technology stack with categories

## Output Guidelines
- Start the final output with "Company Report: [Company Name]"
- Begin with "1) Business Model" and end with "11) Apollo.io Enrichment"
- Format the response using headings and bullet points
- Ensure the output is in plain text format, avoiding markdown
- Cite all references and source links for each point mentioned in each section
- If information for a particular section is not available, note this and move to the next section

## Note
If any tool fails to provide results, use alternative methods or note the lack of information and proceed to the next section.
"""
class SalesResearchBot():
    def __init__(self) -> None:
        # Get API KEY from environment file
        os.environ['OPENAI_API_KEY'] =os.getenv("OPENAI_API_KEY")
        os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY")
        os.environ["APOLLO_API_KEY"] = os.getenv("APOLLO_IO_API_KEY")
    
    def setup_tools(self):
        """Set up tools for the agent."""
        tavily_search_tool = TavilySearchResults()
        apollo_org_tool = Tool(
            name="apollo_io_organization_enrichment",
            func=self.get_apollo_org_details,
            description="""Use this tool to get detailed organization information from Apollo.io 
            using a domain name. Provide only URL of the domain example: www.apollo.io, www.amazon.com.""",
        )
        apollo_people_tool = Tool(
            name="apollo_io_people_enrichment",
            func=self.get_apollo_org_details,
            description="""Use this tool to get detailed information about a person from Apollo.io 
            using the person's first name, last name, company name and company domain. 
            Provide detials as seen these two examples: (Tim, Zheng, Apollo IO, www.apollo.io), (Andy, Jassy, Amazon, www.amazon.com).""",
        )
        tools = [tavily_search_tool,apollo_org_tool]
        return tools

    def setup_agent(self,tools):
        """Set up the agent with tools and prompt."""
        template = PROMPT

        llm = ChatOpenAI(model=MODEL, temperature=0)
        prompt = hub.pull("hwchase17/openai-functions-agent")
        prompt.messages[0] = SystemMessagePromptTemplate(prompt=PromptTemplate(input_variables=[], template=template))
        agent = create_openai_tools_agent(llm, tools, prompt)
        agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
        return agent_executor
    
    def get_apollo_org_details(self, domain):
        """Get organization details from Apollo.io API."""
        url = "https://api.apollo.io/v1/organizations/enrich"
        querystring = {"domain": domain}
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': os.getenv("APOLLO_IO_API_KEY")
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    
    def get_apollo_people_details(self, firstName, lastName, organizationName, organizationDomain):
        """Get People details from Apollo.io API."""
        url = "https://api.apollo.io/v1/people/match"
        querystring = {
            "first_name": firstName,
            "last_name": lastName,
            "organization_name": organizationName,
            "domain": organizationDomain,
            "reveal_personal_emails": True,
            "reveal_phone_number": True,
        }
        headers = {
            'Cache-Control': 'no-cache',
            'Content-Type': 'application/json',
            'X-Api-Key': os.getenv("APOLLO_IO_API_KEY")
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        return response.json()
    
    def run_agent(self,website):
        """Main function to run the application."""
        tools = self.setup_tools()
        agent_executor = self.setup_agent(tools)
        output = agent_executor.invoke({"input": website})
        print(output['output'])
        return output['output']
    