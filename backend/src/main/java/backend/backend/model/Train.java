package backend.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalTime;

@Entity
@Table(name = "trains")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Train {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "train_id", nullable = false, unique = true)
    private String trainId;

    @Column(name = "train_name", nullable = false)
    private String trainName;

    @Column(name = "corridor_id", nullable = false)
    private String corridorId;

    @Column(name = "arrival_time", nullable = false)
    private LocalTime arrivalTime;

    @Column(name = "departure_time", nullable = false)
    private LocalTime departureTime;

    @Column(name = "train_type", nullable = false)
    private String trainType;

    @Column(nullable = false)
    private String priority;
}