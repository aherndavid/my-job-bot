import os
 import asyncio
 from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig
 from google import genai

 async def main():
     # 1. Setup Gemini with the new 2026 SDK
     client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
     
     # 2. Configure the Crawler for GitHub Actions (Headless mode)
     browser_config = BrowserConfig(headless=True)
     run_config = CrawlerRunConfig(cache_mode="bypass")

     async with AsyncWebCrawler(config=browser_config) as crawler:
         # 3. Target URL (Update this to your preferred search)
         result = await crawler.arun(
             url="https://news.ycombinator.com/jobs",
             config=run_config
         )
         
         # 4. Use AI to extract the data
         prompt = f"""
         Extract all job listings from this text. 
         Focus on: Role Title, Company, and Link.
         Format as a clean Markdown table.
         
         TEXT:
         {result.markdown[:6000]}
         """
         
         response = client.models.generate_content(
             model="gemini-1.5-flash", 
             contents=prompt
         )
         
         # 5. Save for GitHub Actions
         with open("jobs_found.md", "w") as f:
             f.write(response.text)

 if __name__ == "__main__":
     asyncio.run(main())
