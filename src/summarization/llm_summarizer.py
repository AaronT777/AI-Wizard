import time
from datetime import datetime
from config import DEFAULT_LLM_MODEL

class MeetingSummarizer:
    """
    A class to generate summaries of meeting transcripts using LLMs.
    """
    
    def __init__(self, client=None):
        """
        Initialize the Meeting Summarizer.
        
        Args:
            client: The Together API client instance. If None, use placeholder summarization.
        """
        self.client = client
        self.model = DEFAULT_LLM_MODEL
        
        # Prompt template for meeting summarization
        self.prompt_template = """
        SYSTEM: You are a professional meeting assistant specialized in summarizing meeting content.
        
        INSTRUCTIONS:
        • Identify the main discussion topics of the meeting
        • Extract key decisions and action items
        • Note responsible persons and deadlines (if mentioned)
        • Organize information into concise bullet points
        • Order content by importance
        • Maintain an objective and neutral tone
        • Ensure the summary comprehensively covers all important points
        
        Meeting transcript: {content}
        
        Please provide a structured meeting summary including:
        1. Meeting topic
        2. Key discussion points
        3. Decisions made
        4. Action items (with responsible persons and deadlines, if any)
        5. Next steps
        """
    
    def generate_summary(self, transcript):
        """
        Generate a meeting summary from the transcript.
        
        Args:
            transcript (str): Meeting transcript text
            
        Returns:
            str: Generated meeting summary
        """
        if not transcript or transcript.strip() == "":
            return "Error: Transcript is empty. Please record and transcribe a meeting first."
        
        # Format the prompt with the transcript
        prompt = self.prompt_template.format(content=transcript)
        
        # If no client provided, use placeholder summarization
        if self.client is None:
            return self._generate_placeholder_summary(transcript)
        
        # Use Together API for real summarization
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error generating summary: {str(e)}")
            # Fallback to placeholder if API fails
            return f"Error using API: {str(e)}\n\n" + self._generate_placeholder_summary(transcript)
    
    def _generate_placeholder_summary(self, transcript):
        """
        Generate a placeholder summary when no API client is available.
        This is used for testing or when API keys aren't configured.
        
        Args:
            transcript (str): Meeting transcript text
            
        Returns:
            str: A simple placeholder summary
        """
        # Extract some content for the summary
        words = transcript.split()
        word_count = len(words)
        
        # Get some "topics" (just the most frequent words for this placeholder)
        common_words = self._get_common_words(transcript)
        
        # Simulated processing time based on transcript length
        processing_time = min(2.0, 0.01 * word_count)
        time.sleep(processing_time)
        
        # Create a simple summary
        return f"""
# Meeting Summary

## Meeting Overview
This meeting transcript contains approximately {word_count} words and appears to discuss topics related to {', '.join(common_words[:3])}.

## Key Discussion Points
- The discussion covered topics including {', '.join(common_words[:5])}
- The meeting participants exchanged views on various aspects of the project
- Several points were raised regarding implementation details

## Decisions Made
- Further discussion may be needed to reach concrete decisions
- The team should continue working on the current tasks

## Action Items
1. Review the full transcript for more detailed information
2. Consider scheduling a follow-up meeting
3. Prepare any necessary documents related to {common_words[0] if common_words else "the project"}

## Next Steps
- Determine priorities based on the discussion
- Allocate resources accordingly
- Plan follow-up meetings as needed

*Note: This is a placeholder summary. For a more accurate and detailed summary, please set up the Together API key.*
        """
    
    def _get_common_words(self, text, min_length=4, max_words=10):
        """
        Get the most common words in the text for the placeholder summary.
        
        Args:
            text (str): The text to analyze
            min_length (int): Minimum length of words to consider
            max_words (int): Maximum number of words to return
            
        Returns:
            list: List of common words
        """
        # Simple word frequency analysis
        words = text.lower().split()
        word_freq = {}
        
        # Common English stopwords to exclude
        stopwords = set([
            "the", "and", "that", "this", "with", "for", "was", "were", "have", 
            "from", "they", "their", "what", "when", "where", "which", "there"
        ])
        
        for word in words:
            # Clean the word of punctuation
            clean_word = ''.join(c for c in word if c.isalnum())
            if len(clean_word) >= min_length and clean_word not in stopwords:
                word_freq[clean_word] = word_freq.get(clean_word, 0) + 1
        
        # Sort by frequency
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, _ in sorted_words[:max_words]]