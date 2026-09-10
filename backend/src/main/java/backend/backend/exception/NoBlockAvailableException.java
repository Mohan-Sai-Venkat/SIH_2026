package backend.backend.exception;

public class NoBlockAvailableException extends RuntimeException {

    public NoBlockAvailableException(String message) {
        super(message);
    }
}