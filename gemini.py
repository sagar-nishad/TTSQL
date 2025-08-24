from google import genai
from google.genai import types

from data import *

from sql import SQL
# ==================================
# GEMINI CLASS
# ==================================
class GeminiSQL:
    def __init__(self, sql_instance: SQL, model_name="gemini-2.5-flash"):
        self.sql = sql_instance
        self.client = genai.Client(api_key=GEMINI_API_KEY)
        self.SYSTEM_PROMPT = """
You are an AI SQL assistant.  
Your task is to convert natural language questions into valid SQL queries.  

Rules:  
- Output only the SQL query, nothing else.  
- Queries must strictly follow MySQL 8.0 syntax and functions.  
- Do not include explanations, comments, markdown formatting (```), or the word "SQL".  
- Always produce syntactically correct SQL that can be executed directly.  
- Every query must end with a semicolon (;).  
    """
        
    def get_query_from_gemini(self, user_input: str) -> str:
   
        schema_info = self.sql.get_all_schemas()
        prompt = f"""
SCHEMA of all the tables present in the database :
{schema_info}

USER REQUEST:
{user_input}
"""
        print(prompt)
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            config=types.GenerateContentConfig(
                system_instruction=self.SYSTEM_PROMPT),
            contents=prompt
        ).text
        # response = "select * from users ;"
        return response

    def execute_with_gemini(self, query: str):
        return self.sql.execute_query(query)



if __name__ == "__main__":

    db = SQL(user=USER, password=PASSWWORD, database=DATABASE)
    db.connect()
    gemini = GeminiSQL(db)

    user_question = " display everything in the user table  "
    query =gemini.get_query_from_gemini(user_question)

    print("Query :", query)

    res = gemini.execute_with_gemini(query)
   

    # db.close()
