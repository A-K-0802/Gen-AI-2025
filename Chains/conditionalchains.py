from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable import RunnableParallel, RunnableBranch, RunnableLambda
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from typing import Literal

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id='mistralai/Mistral-7B-Instruct-v0.2',
    task='text-generation'
)

model=ChatHuggingFace(llm=llm)

class Feedback(BaseModel):
    sentiment:Literal['Positive','Negative'] = Field(description='This is the sentiment of the feedback')

parser_py=PydanticOutputParser(pydantic_object=Feedback)

parser=StrOutputParser()

prompt1=PromptTemplate(
    template='Classify the following feedback into positive or negative.\n {feedback} \n {format_instruction}',
    input_variables=['feedback'],
    partial_variables={'format_instruction': parser_py.get_format_instructions()}
)

prompt2=PromptTemplate(
    template='Write a appropriate response to this positive feedback.\n {feedback}',
    input_variables=['feedback']
)

prompt3=PromptTemplate(
    template='Write a appropriate response to this negative feedback.\n {feedback}',
    input_variables=['feedback']
)

Classifierchain= prompt1 |  model | parser_py


branch_chain=RunnableBranch(
    (lambda x:x.sentiment=='Positive', prompt2|model|parser),
    (lambda x:x.sentiment=='Negative', prompt3|model|parser),
    RunnableLambda(lambda x:'could not find sentiment')
)

chain= Classifierchain | branch_chain

final=chain.invoke({'feedback':"This is a terrible phone."})

print(final)