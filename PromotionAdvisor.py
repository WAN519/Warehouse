import os
from dotenv import load_dotenv  # load .env file
from google import genai
from google.genai.errors import APIError

class PromotionAdvisor:
      def __init__(self, env_file = 'config.env'):
          # Initialization class

          #load API
          load_dotenv('config.env')
          # get API KEY
          api_key = os.environ.get("GEMINI_API_KEY")

          if not api_key:
              raise EnvironmentError(
                  "Error：Can't find 'GEMINI_API_KEY'. Please check your key in the config.env file."
              )

          # Initialization Gemini
          self.client = genai.Client(api_key = api_key)

          # model type: Gemimi-2.5-flash is free with few data
          self.model_name = "gemini-2.5-flash"

          print("PromotionAdvisor initialized and connected to Gemini API.")

      def get_suggestions(self, product_data: list) -> str:
          """
          get data from database, use Gemini API get advisor

          Args:
              product_data: the dict with product information

          Returns:
              return suggestions as Markdown
          """
          # convert to  string that fit to Prompt
          data_for_prompt = "\n".join([str(item) for item in product_data])

          # Define the task for Gemini
          prompt = f"""
          Based on the product data provided below, please give me targeted promotional suggestions.
          Please present the suggestions in a Markdown table with three columns: 'Product Name', 'Analysis', and 'Promotional Strategy'.
          Here is the product data (analyze stock vs. sales):
          {data_for_prompt}
          """

          print(f"\n--- Sending request to {self.model_name}... ---")

          # --- API Call and Return Logic ---
          try:
              response = self.client.models.generate_content(
                 model=self.model_name,
                 contents=prompt
              )
              return response.text

          except APIError as e:
              return f"\n API Call Failed (Status: {e.status_code}), please check your key and network connection: {e.message}"
          except Exception as e:
              return f"\nAn unexpected error occurred: {e}"
