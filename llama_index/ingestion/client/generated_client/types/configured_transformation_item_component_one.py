# This file was auto-generated by Fern from our API Definition.

import typing

from .code_node_parser import CodeNodeParser
from .entity_extractor import EntityExtractor
from .hierarchical_node_parser import HierarchicalNodeParser
from .html_node_parser import HtmlNodeParser
from .hugging_face_embedding import HuggingFaceEmbedding
from .json_node_parser import JsonNodeParser
from .keyword_extractor import KeywordExtractor
from .markdown_node_parser import MarkdownNodeParser
from .marvin_metadata_extractor import MarvinMetadataExtractor
from .open_ai_embedding import OpenAiEmbedding
from .questions_answered_extractor import QuestionsAnsweredExtractor
from .sentence_aware_node_parser import SentenceAwareNodeParser
from .sentence_window_node_parser import SentenceWindowNodeParser
from .simple_file_node_parser import SimpleFileNodeParser
from .summary_extractor import SummaryExtractor
from .title_extractor import TitleExtractor
from .token_aware_node_parser import TokenAwareNodeParser

ConfiguredTransformationItemComponentOne = typing.Union[
    KeywordExtractor,
    TitleExtractor,
    EntityExtractor,
    MarvinMetadataExtractor,
    SummaryExtractor,
    QuestionsAnsweredExtractor,
    SentenceWindowNodeParser,
    HierarchicalNodeParser,
    CodeNodeParser,
    SentenceAwareNodeParser,
    TokenAwareNodeParser,
    HtmlNodeParser,
    MarkdownNodeParser,
    JsonNodeParser,
    SimpleFileNodeParser,
    OpenAiEmbedding,
    HuggingFaceEmbedding,
]