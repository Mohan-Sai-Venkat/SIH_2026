package backend.backend.repository;

import backend.backend.model.Train;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.List;

public interface TrainRepository extends JpaRepository<Train, Long> {

    List<Train> findByCorridorId(String corridorId);

}