package backend.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalDateTime;

@Entity
@Table(
        name = "block_requests",
        uniqueConstraints = {
                @UniqueConstraint(
                        name = "uk_block_request_duplicate",
                        columnNames = {
                                "task_id",
                                "corridor_id",
                                "requested_start",
                                "requested_end"
                        }
                )
        }
)
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class BlockRequest {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "block_id", nullable = false, unique = true)
    private String blockId;

    @Column(name = "task_id", nullable = false)
    private String taskId;

    @Column(name = "corridor_id", nullable = false)
    private String corridorId;

    @Column(name = "requested_start", nullable = false)
    private LocalDateTime requestedStart;

    @Column(name = "requested_end", nullable = false)
    private LocalDateTime requestedEnd;

    @Column(name = "requested_duration", nullable = false)
    private Integer requestedDuration;

    @Column(nullable = false)
    private String department;

    @Column(name = "request_status", nullable = false)
    private String requestStatus;
}