"""Script to generate educational podcasts from input content and concepts.

Usage:
    poetry run python -m main.py splk-1002-pt6
"""

import sys

from podcastfy.client import generate_podcast  # type: ignore


def load_concepts(input_dir):
    """Load concepts from the input directory's concepts file."""
    concepts_file = f"inputs/{input_dir}/concepts"
    with open(concepts_file, "r", encoding="utf-8") as f:
        return [line.strip() for line in f.readlines()]


def load_content(input_dir):
    """Load content from the input directory's content file."""
    content_file = f"inputs/{input_dir}/content"
    with open(content_file, "r", encoding="utf-8") as f:
        return f.read()


def create_dialogue_structure(concept_list):
    """Create a dialogue structure based on the provided concepts."""
    structure = ["Introduce List of concepts"]

    # Add short introductions
    for concept in concept_list:
        structure.append(f"explanation of {concept}")

    structure.append("Closing Remarks")
    return structure


# Get input parameter from command line args
if len(sys.argv) != 2:
    print("Usage: poetry run python -m main.py <input-name>")
    sys.exit(1)
input_name = sys.argv[1]

# Load concepts and content from files
concepts = load_concepts(input_name)
raw_text = load_content(input_name)

config = {
    "word_count": 5000,
    "conversation_style": [
        "Lecture like",
        "Educational",
        "formal",
        "analytical",
        "critical",
    ],
    "roles_person1": "Lecturer",
    "roles_person2": "Lecturer assistant, counterargument provider",
    "dialogue_structure": create_dialogue_structure(concepts),
    "podcast_name": "Splunk Core Certified Power User Exam Preparation",
    "output_language": "English",
    "user_instructions": "Make it correct and accurate; never lie always produce accureate information",
    "engagement_techniques": [
        "Rhetorical Questions",
        "Examples",
        "Analogies",
    ],
    "creativity": 0,
}

print(config)
print(raw_text)

tech_debate_podcast = generate_podcast(
    text=raw_text,
    longform=True,
    conversation_config=config,
    tts_model="openai",
)
