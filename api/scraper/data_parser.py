from langchain_core.output_parsers import JsonOutputParser
from typing import Type
from pydantic import BaseModel


def parse_data(pydantic_class: Type[BaseModel]):
    return JsonOutputParser(pydantic_object=pydantic_class)
