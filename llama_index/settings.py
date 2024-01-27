from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, List, Optional

if TYPE_CHECKING:
    from llama_index import ServiceContext


from llama_index.callbacks.base import BaseCallbackHandler, CallbackManager
from llama_index.core.embeddings.base import BaseEmbedding
from llama_index.embeddings.utils import resolve_embed_model
from llama_index.indices.prompt_helper import PromptHelper
from llama_index.llms import LLM
from llama_index.llms.utils import resolve_llm
from llama_index.node_parser import NodeParser, SentenceSplitter
from llama_index.schema import TransformComponent
from llama_index.types import PydanticProgramMode
from llama_index.utils import get_tokenizer, set_global_tokenizer


@dataclass
class _Settings:
    """Settings for the Llama Index, lazily initialized."""

    # lazy initialization
    _llm: Optional[LLM] = None
    _embed_model: Optional[BaseEmbedding] = None
    _callback_manager: Optional[CallbackManager] = None
    _tokenizer: Optional[Callable[[str], List[Any]]] = None
    _node_parser: Optional[NodeParser] = None
    _prompt_helper: Optional[PromptHelper] = None
    _transformations: Optional[List[TransformComponent]] = None

    # ---- LLM ----

    @property
    def llm(self) -> LLM:
        """Get the LLM."""
        if self._llm is None:
            self._llm = resolve_llm("default")
        return self._llm

    @llm.setter
    def llm(self, llm: LLM) -> None:
        """Set the LLM."""
        self._llm = llm

    @property
    def pydantic_program_mode(self) -> PydanticProgramMode:
        """Get the pydantic program mode."""
        return self.llm.pydantic_program_mode

    @pydantic_program_mode.setter
    def pydantic_program_mode(self, pydantic_program_mode: PydanticProgramMode) -> None:
        """Set the pydantic program mode."""
        self.llm.pydantic_program_mode = pydantic_program_mode

    # ---- Embedding ----

    @property
    def embed_model(self) -> BaseEmbedding:
        """Get the embedding model."""
        if self._embed_model is None:
            self._embed_model = resolve_embed_model("default")
        return self._embed_model

    @embed_model.setter
    def embed_model(self, embed_model: BaseEmbedding) -> None:
        """Set the embedding model."""
        self._embed_model = embed_model

    # ---- Callbacks ----

    @property
    def global_handler(self) -> Optional[BaseCallbackHandler]:
        """Get the global handler."""
        import llama_index

        # TODO: deprecated?
        return llama_index.global_handler

    @global_handler.setter
    def global_handler(self, eval_mode: str, **eval_params: Any) -> None:
        """Set the global handler."""
        from llama_index import set_global_handler

        # TODO: deprecated?
        set_global_handler(eval_mode, **eval_params)

    @property
    def callback_manager(self) -> CallbackManager:
        """Get the callback manager."""
        if self._callback_manager is None:
            self._callback_manager = CallbackManager()
        return self._callback_manager

    @callback_manager.setter
    def callback_manager(self, callback_manager: CallbackManager) -> None:
        """Set the callback manager."""
        self._callback_manager = callback_manager

    # ---- Tokenizer ----

    @property
    def tokenizer(self) -> Callable[[str], List[Any]]:
        """Get the tokenizer."""
        if self._tokenizer is None:
            self._tokenizer = get_tokenizer()

        return self._tokenizer

    @tokenizer.setter
    def tokenizer(self, tokenizer: Callable[[str], List[Any]]) -> None:
        """Set the tokenizer."""
        self._tokenizer = tokenizer

        # TODO: deprecated
        set_global_tokenizer(tokenizer)

    # ---- Node parser ----

    @property
    def node_parser(self) -> NodeParser:
        """Get the node parser."""
        if self._node_parser is None:
            self._node_parser = SentenceSplitter()

        return self._node_parser

    @node_parser.setter
    def node_parser(self, node_parser: NodeParser) -> None:
        """Set the node parser."""
        self._node_parser = node_parser

    @property
    def chunk_size(self) -> int:
        """Get the chunk size."""
        if hasattr(self.node_parser, "chunk_size"):
            return self.node_parser.chunk_size
        else:
            raise ValueError("Configured node parser does not have chunk size.")

    @chunk_size.setter
    def chunk_size(self, chunk_size: int) -> None:
        """Set the chunk size."""
        if hasattr(self.node_parser, "chunk_size"):
            self.node_parser.chunk_size = chunk_size
        else:
            raise ValueError("Configured node parser does not have chunk size.")

    @property
    def chunk_overlap(self) -> int:
        """Get the chunk overlap."""
        if hasattr(self.node_parser, "chunk_overlap"):
            return self.node_parser.chunk_overlap
        else:
            raise ValueError("Configured node parser does not have chunk overlap.")

    @chunk_overlap.setter
    def chunk_overlap(self, chunk_overlap: int) -> None:
        """Set the chunk overlap."""
        if hasattr(self.node_parser, "chunk_overlap"):
            self.node_parser.chunk_overlap = chunk_overlap
        else:
            raise ValueError("Configured node parser does not have chunk overlap.")

    # ---- Node parser alias ----

    @property
    def text_splitter(self) -> NodeParser:
        """Get the text splitter."""
        return self.node_parser

    @text_splitter.setter
    def text_splitter(self, text_splitter: NodeParser) -> None:
        """Set the text splitter."""
        self.node_parser = text_splitter

    # ---- Prompt helper ----
    @property
    def prompt_helper(self) -> PromptHelper:
        """Get the prompt helper."""
        if self._llm is not None and self._prompt_helper is None:
            self._prompt_helper = PromptHelper.from_llm_metadata(self._llm.metadata)
        elif self._prompt_helper is None:
            self._prompt_helper = PromptHelper()

        return self._prompt_helper

    @prompt_helper.setter
    def prompt_helper(self, prompt_helper: PromptHelper) -> None:
        """Set the prompt helper."""
        self._prompt_helper = prompt_helper

    @property
    def num_output(self) -> int:
        """Get the number of outputs."""
        return self.prompt_helper.num_output

    @num_output.setter
    def num_output(self, num_output: int) -> None:
        """Set the number of outputs."""
        self.prompt_helper.num_output = num_output

    @property
    def context_window(self) -> int:
        """Get the context window."""
        return self.prompt_helper.context_window

    @context_window.setter
    def context_window(self, context_window: int) -> None:
        """Set the context window."""
        self.prompt_helper.context_window = context_window

    # ---- Transformations ----
    @property
    def transformations(self) -> List[TransformComponent]:
        """Get the transformations."""
        if self._transformations is None:
            self._transformations = [self.node_parser]
        return self._transformations

    @transformations.setter
    def transformations(self, transformations: List[TransformComponent]) -> None:
        """Set the transformations."""
        self._transformations = transformations


# Singleton
Settings = _Settings()


# -- Helper functions for deprecation/migration --


def llm_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> LLM:
    """Get settings from either settings or context."""
    if context is not None:
        return context.llm

    return settings.llm


def embed_model_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> BaseEmbedding:
    """Get settings from either settings or context."""
    if context is not None:
        return context.embed_model

    return settings.embed_model


def callback_manager_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> CallbackManager:
    """Get settings from either settings or context."""
    if context is not None:
        return context.callback_manager

    return settings.callback_manager


def node_parser_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> NodeParser:
    """Get settings from either settings or context."""
    if context is not None:
        return context.node_parser

    return settings.node_parser


def prompt_helper_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> PromptHelper:
    """Get settings from either settings or context."""
    if context is not None:
        return context.prompt_helper

    return settings.prompt_helper


def transformations_from_settings_or_context(
    settings: _Settings, context: Optional["ServiceContext"]
) -> List[TransformComponent]:
    """Get settings from either settings or context."""
    if context is not None:
        return context.transformations

    return settings.transformations