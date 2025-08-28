import React from "react";

interface ResetButtonProps {
  text: string;
  isDisabled?: boolean;
  onClick: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
}

export const ResetButton: React.FC<ResetButtonProps> = ({
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
      className={className}
    >
      {text}
    </button>
  );
};
