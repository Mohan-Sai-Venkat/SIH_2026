package backend.backend.repository;

import backend.backend.model.Corridor;
import org.springframework.data.jpa.repository.JpaRepository;

import java.util.Optional;

public interface CorridorRepository extends JpaRepository<Corridor, Long> {

    Optional<Corridor> findByCorridorId(String corridorId);

}