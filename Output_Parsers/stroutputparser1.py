from langchain_huggingface import ChatHuggingFace,HuggingFaceEndpoint
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

llm=HuggingFaceEndpoint(
    repo_id='mistralai/Mistral-7B-Instruct-v0.2',
    task='text-generation'
)

model=ChatHuggingFace(llm=llm)

template_1=PromptTemplate(
    template='Write a detailed report on {topic}',
    input_variables=['topic']
)


template_2=PromptTemplate(
    template='Write a detailed summary on following text./n {text}',
    input_variables=['text']
)

parser=StrOutputParser()

chain= template_1 | model | parser | template_2 | model | parser

result=chain.invoke({'topic':'Blackhole'})

print(result)