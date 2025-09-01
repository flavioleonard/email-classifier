import { useState, useRef } from "react";
import { ClassificationResult } from "@/app/interfaces/ClassificationResult";
import { CleanButton } from "@/app/components/buttons/clean-button/CleanButton";
import { SubmitButton } from "@/app/components/buttons/submit-button/SubmitButton";
import "./BoxEmail.css";

interface BoxEmailProps {
  setResult: (result: ClassificationResult) => void;
}
export const BoxEmail = ({ setResult }: BoxEmailProps) => {
  const [emailText, setEmailText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setEmailText("");
    }
  };

  const handleTextChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    setEmailText(event.target.value);
    if (event.target.value && selectedFile) {
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    }
  };

  const resetForm = () => {
    setEmailText("");
    setSelectedFile(null);
    setResult({ category: null, suggestedResponse: "" });
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();

    if (!emailText && !selectedFile) {
      alert("Por favor, insira um texto de email ou selecione um arquivo.");
      return;
    }

    setIsLoading(true);

    try {
      const formData = new FormData();

      if (selectedFile) {
        formData.append("file", selectedFile);
      } else {
        formData.append("text", emailText);
      }

      const response = await fetch(`${API_URL}/api/classify-email`, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Erro na classificação do email");
      }

      const data = await response.json();

      setResult({
        category: data.category,
        suggestedResponse: data.suggested_response,
      });
    } catch (error) {
      console.error("Erro ao processar email:", error);
      alert("Erro ao processar o email. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="box-email">
      <h2>Enviar Email para Análise</h2>

      <form onSubmit={handleSubmit} className="upload-form">
        <div className="input-group">
          <label htmlFor="file-upload">Upload de Arquivo (.txt, .pdf):</label>
          <input
            id="file-upload"
            type="file"
            accept=".txt,.pdf"
            onChange={handleFileChange}
            disabled={isLoading}
            ref={fileInputRef}
          />
          {selectedFile && (
            <p className="file-info">
              Arquivo selecionado: {selectedFile.name}
            </p>
          )}
        </div>

        <div className="input-group">
          <label htmlFor="email-text">Ou cole o texto do email:</label>
          <textarea
            id="email-text"
            value={emailText}
            onChange={handleTextChange}
            placeholder="Cole aqui o conteúdo do email que deseja analisar..."
            rows={8}
            disabled={isLoading}
          />
        </div>

        <div className="button-group">
          <SubmitButton
            text="Analisar Email"
            loadingText="Processando..."
            isLoading={isLoading}
            isDisabled={!emailText && !selectedFile}
          />

          <CleanButton
            text="Limpar"
            onClick={resetForm}
            isDisabled={isLoading}
          />
        </div>
      </form>
    </div>
  );
};
