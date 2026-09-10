package backend.backend.dto;

import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;

import java.time.LocalDate;

public record GeneratePlanRequest(

        @NotNull(message = "Date is required")
        LocalDate date,

        @NotBlank(message = "Corridor ID is required")
        String corridorId,

        @NotBlank(message = "Department is required")
        String department,

        @NotNull(message = "Duration is required")
        @Min(value = 1, message = "Duration must be greater than zero")
        Integer duration,

        @NotBlank(message = "Priority is required")
        String priority,

        @NotBlank(message = "Task ID is required")
        String taskId

) {
}