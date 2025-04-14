from langchain.agents import initialize_agent, AgentType
from langchain_groq import ChatGroq
from langchain_openai import ChatOpenAI
from config import GROQ_API_KEY,OPENAPI_API_KEY
from tools import *
from langchain.tools import Tool

# Initialize the LLM
llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="Meta-Llama/Llama-4-Scout-17b-16e-Instruct"
)

# llm=ChatOpenAI(
#     model="gpt-4",
#     openai_api_key=OPENAPI_API_KEY
#     )

# Create tool list
# tools = [
#     get_all_jobs_ids,
#     get_latest_job_id,
#     get_source_file_name_for_duplicates,
#     get_target_file_name_for_duplicates,
#     get_source_records_count_for_duplicates,
#     get_target_records_count_for_duplicates,

# ]



tools = [
    Tool(
        name="Get all job ids",
        func=get_all_jobs_ids,
        description="Get all folder names in the data folder which are Job IDs"
    ),
    Tool(
        name="Get latest job id",
        func=get_latest_job_id,
        description="Get the latest job ID"
    ),
    Tool(
        name="Get source file name for duplicates",
        func=get_source_file_name_for_duplicates,
        description="Get the source file name for duplicates. Source file name for duplicates starts with s1_duplicates and ends with the <job_id>.csv"
    ),
    Tool(
        name="Get target file name for duplicates",
        func=get_target_file_name_for_duplicates,
        description="Get the target file name for duplicates. Target file name for duplicates starts with s2_duplicates and ends with the <job_id>.csv"
    ),
    Tool(
        name="Get source records count for duplicates",
        func=get_source_records_count_for_duplicates,
        description=(                
            "Get the number of records in the source file for duplicates. "
            "The source file name should start with 's1_duplicates_' and end with the <job_id>.csv"
        )
        
    ),
    Tool(
        name="Get target records count for duplicates",
        func=get_target_records_count_for_duplicates,
        description=(                
            "Get the number of records in the target file for duplicates. "
            "The source file name should start with 's2_duplicates_' and end with the <job_id>.csv"
        )
    ),
    Tool(
        name="Get source records count for unique records",
        func=get_source_records_count_for_unique_records,  
        description=(
            "Get the number of records in the source file for unique records. "
            "The source file name should start with 's1_not_in_s2_' and end with the <job_id>.csv"
        )
    ),
    Tool(
        name="Get target records count for unique records",
        func=get_target_records_count_for_unique_records,
        description=(
            "Get the number of records in the target file for unique records. "
            "The source file name should start with 's2_not_in_s1_' and end with the <job_id>.csv"
        )
    ),
    # Tool(
    #     name="read_mismatched_records",
    #     func=read_mismatched_records,
    #     description=(
    #         "Read msimatched records from the mismatch files. "
    #         "The mismatch file name should start with 'mismatch_' and end with the <job_id>.csv"
    #     )
    # ),
    Tool(
        name="get mismatched record reason",
        func=get_mismatch_record_reason,
        description=(
            "Get the reason for mismatched records. "
            "The mismatch file name should start with 'mismatch_' and end with the <job_id>.csv"
            "It Should compare the source and target column and provide the reason for the mismatch. "
            "The actual column name starts after _ and before _ is source or target name."
            "Please provide the output in humain readble format."
        )


    ),
]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)
