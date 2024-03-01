from google.cloud import translate


def translate_text_with_glossary(
    text: str = "YOUR_TEXT_TO_TRANSLATE",
    target:str = 'ml',
    project_id: str = "numeric-chassis-395210",
) -> translate.TranslateTextResponse:
    """Translates a given text using a glossary.

    Args:
        text: The text to translate.
        project_id: The ID of the GCP project that owns the glossary.
        glossary_id: The ID of the glossary to use.

    Returns:
        The translated text."""
    client = translate.TranslationServiceClient()
    location = "us-central1"
    parent = f"projects/{project_id}/locations/{location}"

    # Supported language codes: https://cloud.google.com/translate/docs/languages
    response = client.translate_text(
        request={
            "contents": [text],
            "target_language_code": target,
            "source_language_code": "en",
            "parent": parent,
        }
    )
    return response.translations[0].translated_text

    
# from google.cloud import translate_v3 as translate

