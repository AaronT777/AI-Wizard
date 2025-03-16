import os
import gradio as gr
import time
from datetime import datetime
from config import APP_TITLE, APP_DESCRIPTION

def create_interface(transcriber, summarizer, save_dir="./data/saved_meetings"):
    """
    Create the Gradio interface for the Meeting Transcription app.
    
    Args:
        transcriber: The WhisperTranscriber instance
        summarizer: The MeetingSummarizer instance
        save_dir: Directory to save meeting transcriptions and summaries
        
    Returns:
        gr.Blocks: Gradio interface
    """
    # Ensure the save directory exists
    os.makedirs(save_dir, exist_ok=True)
    
    # App state
    state = {
        "audio_path": None,
        "transcript": None,
        "summary": None,
        "session_id": None
    }
    
    # Helper functions
    def update_status(message, is_error=False):
        if is_error:
            return f"### Status: ❌ {message}"
        return f"### Status: ✅ {message}"
    
    def generate_session_id():
        """Generate a unique session ID for this meeting."""
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        return f"meeting-{timestamp}"
    
    def file_uploaded(audio_path):
        """Called when an audio file is uploaded."""
        if audio_path is None:
            return update_status("No file uploaded", True)
        
        state["audio_path"] = audio_path
        state["session_id"] = generate_session_id()
        return update_status(f"Audio file uploaded successfully: {os.path.basename(audio_path)}")
    
    def transcribe_audio(audio_path):
        """Transcribe the uploaded audio."""
        if not audio_path:
            return update_status("No audio file uploaded. Please upload an audio file first.", True), None
        
        try:
            state["audio_path"] = audio_path
            status = update_status("Transcribing audio... This may take a moment.")
            
            # Call the transcriber
            transcript = transcriber.transcribe(audio_path)
            
            # Save the transcript
            if transcript and state["session_id"]:
                transcript_path = os.path.join(save_dir, f"{state['session_id']}_transcript.txt")
                with open(transcript_path, "w", encoding="utf-8") as f:
                    f.write(transcript)
                print(f"Transcript saved to {transcript_path}")
            
            state["transcript"] = transcript
            return update_status("Transcription complete"), transcript
        except Exception as e:
            import traceback
            error_trace = traceback.format_exc()
            print(f"Transcription error: {str(e)}")
            print(error_trace)
            return update_status(f"Transcription error: {str(e)}", True), None
    
    def generate_meeting_summary(transcript):
        """Generate a summary of the meeting transcript."""
        if not transcript or transcript.strip() == "":
            return update_status("No transcript available. Please transcribe audio first.", True), None
        
        try:
            status = update_status("Generating summary... This may take a moment.")
            
            # Call the summarizer
            summary = summarizer.generate_summary(transcript)
            
            # Save the summary
            if summary and state["session_id"]:
                summary_path = os.path.join(save_dir, f"{state['session_id']}_summary.txt")
                with open(summary_path, "w", encoding="utf-8") as f:
                    f.write(summary)
                print(f"Summary saved to {summary_path}")
            
            state["summary"] = summary
            return update_status("Summary generation complete"), summary
        except Exception as e:
            return update_status(f"Summary generation error: {str(e)}", True), None
    
    def save_text(text, prefix="meeting"):
        """Save text to a file."""
        if not text or text.strip() == "":
            return "Error: Nothing to save. Content is empty."
        
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"{prefix}_{timestamp}.txt"
        filepath = os.path.join(save_dir, filename)
        
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(text)
            return f"✅ Successfully saved to {filepath}"
        except Exception as e:
            return f"❌ Error saving file: {str(e)}"
    
    def clear_all():
        """Reset the application state."""
        state["audio_path"] = None
        state["transcript"] = None
        state["summary"] = None
        return (
            update_status("All data cleared. Ready to upload a new audio file."),
            None,  # Clear audio
            "",    # Clear transcript
            "",    # Clear summary
            ""     # Clear save status
        )
    
    # Create the Gradio interface
    with gr.Blocks(title=APP_TITLE, theme=gr.themes.Soft(
        primary_hue="blue",
        secondary_hue="indigo",
    )) as interface:
        gr.Markdown(f"# 🎙️ {APP_TITLE}")
        gr.Markdown(f"### {APP_DESCRIPTION}")
        
        # Status indicator
        status_indicator = gr.Markdown("### Status: Ready to upload audio file")
        
        # Audio upload component
        with gr.Row():
            with gr.Column(scale=3):
                audio_input = gr.Audio(
                    sources=["upload"],
                    type="filepath",
                    label="Upload Audio File",
                    elem_id="audio_uploader"
                )
        
        # Transcription section
        with gr.Row():
            transcribe_btn = gr.Button("📝 Transcribe Audio", variant="primary", size="lg")
        
        transcript_output = gr.Textbox(
            label="📄 Meeting Transcript",
            lines=10,
            placeholder="Upload an audio file and click 'Transcribe Audio' button. The transcript will appear here...",
            elem_id="transcript_box"
        )
        
        # Summary section
        with gr.Row():
            summarize_btn = gr.Button("📋 Generate Meeting Summary", variant="secondary", size="lg")
        
        summary_output = gr.Textbox(
            label="✨ Meeting Summary",
            lines=10,
            placeholder="After transcription, click 'Generate Meeting Summary' button. The summary will appear here...",
            elem_id="summary_box"
        )
        
        # Save and clear options
        with gr.Row():
            save_transcript_btn = gr.Button("💾 Save Transcript", size="sm")
            save_summary_btn = gr.Button("💾 Save Summary", size="sm")
            clear_all_btn = gr.Button("🗑️ Clear All", size="sm")
        
        save_status = gr.Markdown("")
        
        # Audio upload event
        audio_input.change(
            fn=file_uploaded,
            inputs=[audio_input],
            outputs=[status_indicator]
        )
        
        # Connect events to handlers
        transcribe_btn.click(
            fn=transcribe_audio,
            inputs=[audio_input],
            outputs=[status_indicator, transcript_output]
        )
        
        summarize_btn.click(
            fn=generate_meeting_summary,
            inputs=[transcript_output],
            outputs=[status_indicator, summary_output]
        )
        
        save_transcript_btn.click(
            fn=lambda x: save_text(x, "transcript"),
            inputs=[transcript_output],
            outputs=[save_status]
        )
        
        save_summary_btn.click(
            fn=lambda x: save_text(x, "summary"),
            inputs=[summary_output],
            outputs=[save_status]
        )
        
        clear_all_btn.click(
            fn=clear_all,
            outputs=[status_indicator, audio_input, transcript_output, summary_output, save_status]
        )
        
        # Footer information
        gr.Markdown("""
        ---
        **Tips:** This tool is suitable for transcribing various audio files, such as meeting recordings, interviews, lectures, etc.
        Supported audio formats include MP3, WAV, M4A, and other common formats.
        """)
    
    return interface