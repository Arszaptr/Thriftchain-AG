"use client";
import { useEffect, useState } from "react";

export default function Home() {
  const [status, setStatus] = useState("Loading...");

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/test`)
      .then((res) => res.json())
      .then((data) => setStatus(data.data))
      .catch(() => setStatus("Gagal konek ke backend"));
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <h1 className="text-4xl font-bold mb-8">Thriftchain-AG</h1>
      <div className="bg-gray-100 rounded-lg p-6 text-center">
        <p className="text-gray-500 mb-2">Status Backend:</p>
        <p className="text-2xl font-semibold text-green-600">{status}</p>
      </div>
    </main>
  );
}