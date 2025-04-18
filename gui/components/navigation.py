#clockpilot/gui/components/navigation.py
def setup_navigation(root, frames):
    """Configura la navegación entre frames."""
    def show_frame(frame):
        """Función para cambiar entre pantallas y actualizar datos si es necesario."""
        if hasattr(frame, "update_results"):
            frame.update_results()
        if hasattr(frame, "update_breakdown"):
            frame.update_breakdown()
        frame.tkraise()

    root.show_frame = show_frame

    # Asignar referencias entre frames
    for frame_name, frame in frames.items():
        frame.show_frame = show_frame
        for other_frame_name, other_frame in frames.items():
            if other_frame_name != frame_name:
                setattr(frame, f"{other_frame_name}_frame", other_frame)