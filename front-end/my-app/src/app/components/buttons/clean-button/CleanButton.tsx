import React from "react";
import "./CleanButton.css";

interface CleanButtonProps {
  text: string;
  isDisabled?: boolean;
  onClick: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
}

export const CleanButton: React.FC<CleanButtonProps> = ({
  text,
  isDisabled = false,
  onClick,
  type = "button",
  className = "reset-btn",
}) => {
  return (
    <button
      type={type}
      disabled={isDisabled}
      onClick={onClick}
      className="reset-button"
    >
      {text}
    </button>
  );
};
