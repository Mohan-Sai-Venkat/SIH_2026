package backend.backend.dto;

public record AIInsightResponse(
        String title,
        String message,
        String severity
) {
}