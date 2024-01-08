from langchain.prompts import PromptTemplate
import json


def prompt_gen(query, splitted_content_str, parser, llm):
    prompt = PromptTemplate(
        template="this is scraped from a website.\n\n\n{splitted_content}\n{format_instructions}\n{query}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_llm = prompt | llm | parser

    output = prompt_and_llm.invoke(
        {
            "query": query,
            "splitted_content": splitted_content_str,
        }
    )

    return json.dumps(output)
