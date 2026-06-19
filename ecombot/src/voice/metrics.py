from dataclasses import dataclass


@dataclass
class VoiceMetrics:
    stt_ms: int
    agent_ms: int
    tts_ms: int

    @property
    def total_ms(self):
        return (
            self.stt_ms
            + self.agent_ms
            + self.tts_ms
        )


def print_metrics(metrics):

    print("\n========== LATENCY ==========")

    print(f"STT    : {metrics.stt_ms} ms")
    print(f"Agent  : {metrics.agent_ms} ms")
    print(f"TTS    : {metrics.tts_ms} ms")
    print(f"Total  : {metrics.total_ms} ms")

    print("=============================\n")