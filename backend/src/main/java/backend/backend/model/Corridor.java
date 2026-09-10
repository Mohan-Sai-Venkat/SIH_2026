package backend.backend.model;

import jakarta.persistence.*;
import lombok.*;

import java.time.LocalTime;

@Entity
@Table(name = "corridors")
@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
@Builder
public class Corridor {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(name = "corridor_id", nullable = false, unique = true)
    private String corridorId;

    @Column(name = "from_station", nullable = false)
    private String fromStation;

    @Column(name = "to_station", nullable = false)
    private String toStation;

    @Column(name = "distance_km", nullable = false)
    private Double distanceKm;

    @Column(name = "availability_percent", nullable = false)
    private Double availabilityPercent;

    @Column(name = "available_start", nullable = false)
    private LocalTime availableStart;

    @Column(name = "available_end", nullable = false)
    private LocalTime availableEnd;

    @Column(name = "train_count", nullable = false)
    private Integer trainCount;

    @Column(nullable = false)
    private String status;
}