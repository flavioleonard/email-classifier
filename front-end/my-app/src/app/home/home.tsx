"use client";

import React, { useState } from "react";
import "./home.css";
import { Header } from "../components/header/header";
import { BoxEmail } from "../components/box-email/BoxEmail";
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
        <BoxEmail />

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
