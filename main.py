"""Script to generate educational podcasts from input content and concepts.

Usage:
    poetry run python -m main.py splk-1002-pt1 "Field Extractor" --duration 3
"""

# pylint: disable=import-error
import argparse

from podcastfy.client import generate_podcast  # type: ignore


def load_content(input_file):
    """Load content from the input file."""
    with open(f"inputs/{input_file}", "r", encoding="utf-8") as f:
        return f.read()


def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate educational podcasts from input content."
    )
    parser.add_argument("input_name", help="Name of the input file")
    parser.add_argument("concept_name", help="Name of the concept")
    parser.add_argument(
        "--duration",
        "-d",
        type=int,
        choices=[2, 3, 5, 7],
        help="Duration of the podcast in minutes (2, 3, 5, or 7)",
    )
    return parser.parse_args()


# Parse command line arguments
args = parse_arguments()

# Duration to word count mapping
DURATION_TO_WORDS = {2: 300, 3: 450, 5: 750, 7: 1050}

# Load concepts and content from files
raw_text = load_content(args.input_name)

config = {
    "word_count": DURATION_TO_WORDS.get(
        args.duration, 750
    ),  # Default to 750 words (5 minutes) if duration not specified
    "conversation_style": [
        "Clear",
        "Informative",
        "Structured",
        "Educational",
    ],
    "roles_person1": "Host",
    "roles_person2": "Technical Expert",
    "dialogue_structure": [
        "Introduction",
        "Overview of Topic",
        "Deep Dive",
        "Case Studies/Examples",
        "Q&A Session",
        "Conclusion",
    ],
    "podcast_name": f"Splunk Core Certified Power User - {args.concept_name}",
    "output_language": "English",
    "user_instructions": "Ensure clarity in explanations",
    "engagement_techniques": [
        "Analogies",
        "Real-world Examples",
        "Visual Descriptions",
        "Interactive Q&A",
        "Simplified Explanations",
    ],
}

print(config)

# transcript_file = generate_podcast(
#     text=raw_text,
#     conversation_config=config,
#     transcript_only=True,
#     llm_model_name="o1-mini",
#     api_key_label="OPENAI_API_KEY",
# )

# audio_file_from_transcript = generate_podcast(
#     transcript_file=transcript_file,
#     conversation_config=config,
#     tts_model="elevenlabs",
# )
