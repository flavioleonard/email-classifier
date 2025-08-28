import React from "react";
import "./submitButton.css";

interface SubmitButtonProps {
  text: string;
  loadingText?: string;
  isLoading?: boolean;
  isDisabled?: boolean;
  onClick?: () => void;
  type?: "button" | "submit" | "reset";
  className?: string;
}

export const SubmitButton: React.FC<SubmitButtonProps> = ({
  text,
  loadingText = "Processando...",
  isLoading = false,
  isDisabled = false,
  onClick,
  type = "submit",
}) => {
  return (
    <button
      type={type}
      disabled={isLoading || isDisabled}
      onClick={onClick}
      className="button"
    >
      {isLoading ? loadingText : text}
    </button>
  );
};
