"use client";

import React, { useState } from "react";
import "./home.css";
import { Header } from "../components/header/header";
import { BoxEmail } from "../components/box-email/BoxEmail";
import { CopyButton } from "../components/buttons/copy-button/CopyButton";
import { ClassificationResult } from "../interfaces/ClassificationResult";

export const Home = () => {
  const [result, setResult] = useState<ClassificationResult>({
    category: null,
    suggestedResponse: "",
  });

  return (
    <div className="home-container">
      <Header />

      <div className="main-content">
        <BoxEmail setResult={setResult} />

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
                <div className="response-header">
                  <h3>Resposta Automática Sugerida:</h3>
                  <CopyButton textToCopy={result.suggestedResponse} />
                </div>
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
