from openai import OpenAI


class ChatUtils:
    def __init__(self, model: str = "gpt-4o-mini"):
        self.client = OpenAI()
        self.model = model

    def rephrase(self, transcript_snippet: str, metadata: dict) -> str:
        """Rephrase transcript snippet into a concise answer."""
        raw_answer = f"""
        From video: {metadata.get('title', 'Unknown')}
        Time: {metadata.get('start_time')} → {metadata.get('end_time')}
        Transcript snippet: {transcript_snippet}
        """

        completion = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rewrites transcript snippets into concise answers."},
                {"role": "user", "content": f"Rephrase this transcript snippet into a clear answer: {raw_answer}. Do not add extra information"}
            ]
        )
        return completion.choices[0].message.content.strip()
