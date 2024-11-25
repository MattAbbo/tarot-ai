# app/services/langfuse_service.py
from langfuse import Langfuse
import os
from typing import Dict, Any, Optional

class LangfuseService:
    def __init__(self):
        print("Initializing LangfuseService...")
        self.langfuse = Langfuse(
            public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
            secret_key=os.getenv("LANGFUSE_SECRET_KEY")
        )
        print("LangfuseService initialized successfully")
    
    async def track_reading(self, session_id: str, reading_data: Dict[str, Any]) -> None:
        print(f"\n--- Starting track_reading for session {session_id} ---")
        try:
            print("Creating trace...")
            trace = self.langfuse.trace(
                id=session_id,
                name="tarot_reading"
            )

            # Generate spans but don't try to end them
            print("Creating generation span...")
            trace.generation(
                name="card_interpretation",
                model=reading_data["model"],
                model_parameters={
                    "max_tokens": 400
                },
                prompt=[
                    {
                        "role": "system",
                        "content": reading_data["system_prompt"]
                    },
                    {
                        "role": "user",
                        "content": reading_data["user_prompt"]
                    }
                ],
                completion=reading_data["completion"]
            )

            print("Creating metadata span...")
            trace.span(
                name="reading_metadata",
                input={
                    "card_name": reading_data["card_name"],
                    "original_question": reading_data["original_question"],
                    "has_reflection": bool(reading_data["reflection"])
                }
            )

            print("Track reading completed successfully")

        except Exception as e:
            print(f"Error in track_reading: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    async def track_image_interpretation(self, session_id: str, interpretation_data: Dict[str, Any]) -> None:
        print(f"\n--- Starting track_image_interpretation for session {session_id} ---")
        try:
            print("Creating trace...")
            trace = self.langfuse.trace(
                id=session_id,
                name="image_interpretation"
            )

            print("Creating generation span...")
            trace.generation(
                name="image_analysis",
                model=interpretation_data["model"],
                model_parameters={
                    "max_tokens": 400
                },
                prompt=[
                    {
                        "role": "system",
                        "content": interpretation_data["system_prompt"]
                    }
                ],
                completion=interpretation_data["completion"]
            )

            print("Track image interpretation completed successfully")

        except Exception as e:
            print(f"Error in track_image_interpretation: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    def track_error(self, session_id: str, error: str, context: str) -> None:
        print(f"\n--- Starting track_error for session {session_id} ---")
        try:
            print("Creating trace...")
            trace = self.langfuse.trace(
                id=session_id,
                name=f"error_{context}"
            )

            print("Creating error span...")
            trace.span(
                name="error",
                input={
                    "error_message": error,
                    "context": context
                }
            )

            print("Track error completed successfully")

        except Exception as e:
            print(f"Error in track_error: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

    async def score_reading(self, session_id: str, score: float, feedback: Optional[str] = None) -> None:
        print(f"\n--- Starting score_reading for session {session_id} ---")
        try:
            print("Submitting score...")
            self.langfuse.score(
                name="user_satisfaction",
                trace_id=session_id,
                value=score,
                comment=feedback
            )
            print("Score submitted successfully")

        except Exception as e:
            print(f"Error in score_reading: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")

langfuse_service = LangfuseService()