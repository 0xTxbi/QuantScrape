from langchain.prompts import PromptTemplate


def prompt_gen(query, splitted_content_str, parser, llm):
    prompt = PromptTemplate(
        template="you're a high performant data extractor. extract the relevant details you can make up from. for context, {query}\n. strictly ensure you give me the data. don't give me conversational text\n\n\n{splitted_content}\n{format_instructions}\n",
        input_variables=["query"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    prompt_and_llm = prompt | llm | parser

    # formattedPrompt = prompt()
    output = prompt_and_llm.invoke(
        {
            "query": query,
            "splitted_content": splitted_content_str,
        }
    )

    print(output)
    return output
