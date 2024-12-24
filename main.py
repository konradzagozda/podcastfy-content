"""Script to generate educational podcasts from input content and concepts.

Usage:
    poetry run python -m main.py splk-1002-pt1 "Field Extractor" --duration 3
"""

# pylint: disable=import-error
import argparse
import os
from pathlib import Path

from podcastfy.client import generate_podcast  # type: ignore


def load_content(input_file):
    """Load content from the input file."""
    with open(f"inputs/{input_file}", "r", encoding="utf-8") as f:
        return f.read()


def load_user_instructions():
    """Load user instructions from the prompts file."""
    try:
        with open("prompts/user-instructions", "r", encoding="utf-8") as f:
            return f.read().strip().replace("\n", " ; ")
    except FileNotFoundError:
        return "Ensure clarity in explanations"  # Default if file not found


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


def rename_transcript(original_path, model_name, input_name):
    """Rename transcript file to the desired format."""
    if not original_path:
        return None

    # Extract the ID from the original filename
    file_id = Path(original_path).stem.split("_")[-1]

    # Create new filename
    new_filename = f"transcript_{model_name}_{input_name}_{file_id}.txt"
    new_path = os.path.join(os.path.dirname(original_path), new_filename)

    # Rename the file
    try:
        os.rename(original_path, new_path)
        return new_path
    except OSError:
        return original_path


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
    "user_instructions": load_user_instructions(),
    "engagement_techniques": [
        "Analogies",
        "Real-world Examples",
        "Visual Descriptions",
        "Interactive Q&A",
        "Simplified Explanations",
    ],
}

print(config)

# Generate transcript with o1-mini model
transcript_file_o1 = generate_podcast(
    text=raw_text,
    conversation_config=config,
    transcript_only=True,
    llm_model_name="o1-mini",
    api_key_label="OPENAI_API_KEY",
)
transcript_file_o1 = rename_transcript(transcript_file_o1, "o1-mini", args.input_name)

# Generate transcript with default model (gemini)
transcript_file_default = generate_podcast(
    text=raw_text,
    conversation_config=config,
    transcript_only=True,
    llm_model_name="gemini-exp-1206",
)
transcript_file_default = rename_transcript(
    transcript_file_default, "gemini", args.input_name
)

# # Generate audio using the o1-mini transcript
# audio_file_from_transcript_o1 = generate_podcast(
#     transcript_file=transcript_file_o1,
#     conversation_config=config,
#     tts_model="elevenlabs",
# )

# # Generate audio using the default transcript
# audio_file_from_transcript_default = generate_podcast(
#     transcript_file=transcript_file_default,
#     conversation_config=config,
#     tts_model="elevenlabs",
# )
