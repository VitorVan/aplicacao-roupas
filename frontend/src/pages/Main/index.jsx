import React, { useState } from "react";

import httpClient from "../../app/services/httpClient";

import Upload from '../../components/Upload'
import { Button } from "antd";

const locale = {
  emptyText: (
    <div className="w-full flex flex-col items-center mt-6 gap-3">
      <div class="ant-empty-image">
        <svg
          width="64"
          height="41"
          viewBox="0 0 64 41"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g transform="translate(0 1)" fill="none" fill-rule="evenodd">
            <ellipse fill="#f5f5f5" cx="32" cy="33" rx="32" ry="7"></ellipse>
            <g fill-rule="nonzero" stroke="#d9d9d9">
              <path d="M55 12.76L44.854 1.258C44.367.474 43.656 0 42.907 0H21.093c-.749 0-1.46.474-1.947 1.257L9 12.761V22h46v-9.24z"></path>
              <path
                d="M41.613 15.931c0-1.605.994-2.93 2.227-2.931H55v18.137C55 33.26 53.68 35 52.05 35h-40.1C10.32 35 9 33.259 9 31.137V13h11.16c1.233 0 2.227 1.323 2.227 2.928v.022c0 1.605 1.005 2.901 2.237 2.901h14.752c1.232 0 2.237-1.308 2.237-2.913v-.007z"
                fill="#fafafa"
              ></path>
            </g>
          </g>
        </svg>
      </div>
      <div className="text-gray-300 text-center">Nenhum dado encontrado</div>
    </div>
  ),
};

export default function Main() {
  const [data, setData] = useState({});
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const uploadProps = {
    name: "file",
    customRequest: async ({ file, onSuccess, onError }) => {
      try {
        setFile(file);
        const fmData = new FormData();
        fmData.append("file", file);
        const response = await httpClient.post("/upload", fmData);
        setData(response.data);
        return onSuccess("ok");
      } catch (error) {
        console.log(error.message)
        return onError(error);
      }
    },
    headers: {
      authorization: "authorization-text",
    },
    onChange(info) {
      if (info.file.status !== "uploading") {
      }
      if (info.file.status === "done") {
        message.success(`Roupa analisada com sucesso!`);
      } else if (info.file.status === "error") {
        message.error(info.file.error);
      }
    },
    maxCount: 1,
  };

  function handleFileChange(file) {
    if (!file) {
      setFile(null);
      setImageUrl(null);
      return;
    }
    setFile(file);
    setImageUrl(URL.createObjectURL(file));
  }

  async function handleSendFile() {
    if (!file) return;
    try {
      setLoading(true);
      const fmData = new FormData();
      fmData.append("file", file);
      const response = await httpClient.post("/upload", fmData);
      setData(response.data);
    } catch (error) { 
      console.log(error.message)
    }
    setLoading(false);
  }


  return (
    <div className="flex flex-col gap-12 items-center py-16 min-h-screen">
      <h1 className="text-2xl">Detector de roupas</h1>

      <div className="flex flex-col gap-8">

      <Upload onUpload={(file) => setFile(file)} />

      <Button size="large" onClick={handleSendFile} disabled={!file} className="w-full" loading={loading}>Enviar</Button>
      </div>

      <p>
        response: <pre>{JSON.stringify(data, null, 2)}</pre>
      </p>
    </div>
  );
}
