"use client";

import { FormEvent, useState } from "react";

interface Fuente {
  chunk: string;
  distancia: number;
}

interface QueryResult {
  respuesta: string;
  fuentes: Fuente[];
}

const API_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:3001";

export default function Home() {
  const [pregunta, setPregunta] = useState("");
  const [resultado, setResultado] = useState<QueryResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    if (!pregunta.trim()) return;

    setLoading(true);
    setError(null);
    setResultado(null);

    try {
      const response = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ pregunta }),
      });

      if (!response.ok) {
        throw new Error(`Error ${response.status}`);
      }

      const data: QueryResult = await response.json();
      setResultado(data);
    } catch (err) {
      setError(
        err instanceof Error ? err.message : "Ocurrió un error inesperado",
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen flex-col items-center bg-zinc-50 px-4 py-16 dark:bg-black">
      <main className="flex w-full max-w-2xl flex-col gap-8">
        <div className="flex flex-col gap-2">
          <h1 className="text-2xl font-semibold text-black dark:text-zinc-50">
            alquilAI
          </h1>
          <p className="text-zinc-600 dark:text-zinc-400">
            Preguntá sobre la Ley 27.551 de Alquileres.
          </p>
        </div>

        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <textarea
            value={pregunta}
            onChange={(e) => setPregunta(e.target.value)}
            placeholder="¿Cuánto puede pedir de depósito el dueño?"
            rows={3}
            className="w-full resize-none rounded-lg border border-zinc-300 bg-white p-3 text-black outline-none focus:border-zinc-500 dark:border-zinc-700 dark:bg-zinc-900 dark:text-zinc-50"
          />
          <button
            type="submit"
            disabled={loading || !pregunta.trim()}
            className="self-start rounded-full bg-black px-5 py-2 text-white transition-colors hover:bg-zinc-800 disabled:opacity-50 dark:bg-white dark:text-black dark:hover:bg-zinc-200"
          >
            {loading ? "Consultando..." : "Preguntar"}
          </button>
        </form>

        {error && (
          <p className="text-red-600 dark:text-red-400">Error: {error}</p>
        )}

        {resultado && (
          <div className="flex flex-col gap-6">
            <div className="rounded-lg border border-zinc-300 bg-white p-4 dark:border-zinc-700 dark:bg-zinc-900">
              <h2 className="mb-2 text-sm font-medium text-zinc-500 dark:text-zinc-400">
                Respuesta
              </h2>
              <p className="whitespace-pre-wrap text-black dark:text-zinc-50">
                {resultado.respuesta}
              </p>
            </div>

            <div className="flex flex-col gap-2">
              <h2 className="text-sm font-medium text-zinc-500 dark:text-zinc-400">
                Fuentes
              </h2>
              {resultado.fuentes.map((fuente, i) => (
                <details
                  key={i}
                  className="rounded-lg border border-zinc-200 bg-white p-3 text-sm dark:border-zinc-800 dark:bg-zinc-900"
                >
                  <summary className="cursor-pointer text-zinc-600 dark:text-zinc-400">
                    Fuente {i + 1} (distancia: {fuente.distancia.toFixed(3)})
                  </summary>
                  <p className="mt-2 whitespace-pre-wrap text-zinc-700 dark:text-zinc-300">
                    {fuente.chunk}
                  </p>
                </details>
              ))}
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
