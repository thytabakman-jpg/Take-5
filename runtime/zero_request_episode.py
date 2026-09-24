"""Zero-request observation episode through the governed activation bridge."""
from controller_episode import run_episode

def zero_request_episode(corpus, observer):
    """Discover observation work without manufacturing a substantive governing job."""
    if not corpus:
        raise ValueError("corpus required")
    target="corpus:"+"|".join(sorted(str(x) for x in corpus))
    return run_episode(
        episode="zero-request",
        program_id="DOS",
        target_id=target,
        job="OBSERVE_STRUCTURE",
        authority=frozenset({"observe"}),
        observation_only=True,
        worker=lambda binding: observer(corpus,binding),
        environment="zero-request-fixture",
    )
