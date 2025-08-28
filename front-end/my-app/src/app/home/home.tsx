"use client";

import React, { useState } from "react";
import "./home.css";

interface ClassificationResult {
  category: "Produtivo" | "Improdutivo" | null;
  suggestedResponse: string;
}

export const Home = () => {
  const [emailText, setEmailText] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [result, setResult] = useState<ClassificationResult>({
    category: null,
    suggestedResponse: "",
  });

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
      await new Promise((resolve) => setTimeout(resolve, 2000));

      const mockResult: ClassificationResult = {
        category: Math.random() > 0.5 ? "Produtivo" : "Improdutivo",
        suggestedResponse:
          "Esta é uma resposta automática sugerida baseada na análise do email.",
      };

      setResult(mockResult);
    } catch (error) {
      console.error("Erro ao processar email:", error);
      alert("Erro ao processar o email. Tente novamente.");
    } finally {
      setIsLoading(false);
    }
  };

  const resetForm = () => {
    setEmailText("");
    setSelectedFile(null);
    setResult({ category: null, suggestedResponse: "" });
  };

  return (
    <div className="home-container">
      <div className="header">
        <h1>Classificador de Emails</h1>
        <p>
          Classifique emails como Produtivos ou Improdutivos e obtenha respostas
          automáticas sugeridas
        </p>
      </div>

      <div className="main-content">
        <div className="upload-section">
          <h2>Enviar Email para Análise</h2>

          <form onSubmit={handleSubmit} className="upload-form">
            <div className="input-group">
              <label htmlFor="file-upload">
                Upload de Arquivo (.txt, .pdf):
              </label>
              <input
                id="file-upload"
                type="file"
                accept=".txt,.pdf"
                onChange={handleFileChange}
                disabled={isLoading}
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
              <button
                type="submit"
                disabled={isLoading || (!emailText && !selectedFile)}
                className="submit-btn"
              >
                {isLoading ? "Processando..." : "Analisar Email"}
              </button>

              <button
                type="button"
                onClick={resetForm}
                disabled={isLoading}
                className="reset-btn"
              >
                Limpar
              </button>
            </div>
          </form>
        </div>

        {result.category && (
          <div className="results-section">
            <h2>Resultados da Análise</h2>

            <div className="result-card">
              <div className="category-result">
                <h3>Categoria:</h3>
                <span
                  className={`category-badge ${result.category.toLowerCase()}`}
                >
                  {result.category}
                </span>
              </div>

              <div className="response-result">
                <h3>Resposta Automática Sugerida:</h3>
                <div className="suggested-response">
                  {result.suggestedResponse}
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
