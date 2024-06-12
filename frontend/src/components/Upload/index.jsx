import { useEffect, useRef, useState } from "react";
import {
  UploadContainer,
  FileInput,
  UploadButton,
  ImageContainer,
  DeleteButton,
  Image,
  UploadArea,
} from "./styles";

import { LoadingOutlined, DeleteOutlined } from "@ant-design/icons";
import { message } from "antd";

const fileTypesNames = {
  image: "imagem",
  pdf: "PDF",
  video: "vídeo",
  audio: "áudio",
  text: "texto",
  application: "aplicação",
  message: "mensagem",
  multipart: "multipart",
  other: "outro",
  unknown: "desconhecido",
  any: "qualquer",
  none: "nenhum",
};

export default function Upload({ onUpload, accepts, disabled = false }) {
  const fileInputRef = useRef(null);
  const [loading, setLoading] = useState(false);
  const [isFileHovering, setIsFileHovering] = useState(false);
  const [file, setFile] = useState(null);
  const [imageUrl, setImageUrl] = useState(null);

  useEffect(() => {
    onUpload(file);
  }, [file, onUpload]);

  const handleFileChange = (event) => {
    if (!event.target.files) {
      handleSetFile(null);
      return;
    }

    const file = event.target.files[0];
    handleSetFile(file);
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileDrop = (event) => {
    event.preventDefault();
    setIsFileHovering(false);
    const droppedFile = event.dataTransfer.files[0];
    handleSetFile(droppedFile);
  };

  const handleSetFile = (file) => {
    if (file) {
      setLoading(true);
      setFile(null);
      setImageUrl(null);
      setTimeout(() => {
        if (file.size > 1024 * 1024 * 5) {
          alert("O arquivo deve ter no máximo 5MB");
          setLoading(false);
          return;
        }

        if (accepts && !accepts.includes(file.type.split("/")[0])) {
          const acceptedItensNames = accepts.map(
            (accept) => fileTypesNames[accept]
          );
          const messageString =
            "O arquivo deve ser do tipo " +
            acceptedItensNames.join(" ou ") +
            "!";
          message.error({
            content: messageString,
            duration: 4,
          });
          setLoading(false);
          return;
        }

        setFile(file);
        setImageUrl(URL.createObjectURL(file));
        setLoading(false);
      }, 100);
    } else {
      setFile(null);
      setImageUrl(null);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
    setIsFileHovering(true);
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsFileHovering(false);
  };

  const handleDeleteButtonClick = () => {
    // make change on fileinput to trigger onChange event
    fileInputRef.current.value = "";
    handleSetFile(null);
  };

  return (
    <UploadContainer
      onDrop={!disabled ? handleFileDrop : undefined}
      onDragOver={!disabled ? handleDragOver : undefined}
      onDragLeave={!disabled ? handleDragLeave : undefined}
    >
      {imageUrl && (
        <ImageContainer
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          disabled={disabled}
        >
          <DeleteButton
            type="button"
            onClick={handleDeleteButtonClick}
            disabled={disabled}
          >
            <DeleteOutlined />
          </DeleteButton>
          <Image
            src={imageUrl}
            alt="Receipt"
            onClick={handleUploadClick}
            disabled={disabled}
          />
        </ImageContainer>
      )}

      {!imageUrl && (
        <UploadArea
          onClick={handleUploadClick}
          initial={{ opacity: 0, scale: 1.1 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.8 }}
          dragElastic={0.1}
          $isFileHovering={isFileHovering}
          disabled={disabled}
        >
          {loading && <LoadingOutlined />}
          {!loading && (
            <p style={{ marginTop: "40px" }}>Tire a foto da sua roupa</p>
          )}
          <UploadButton
            disabled={disabled}
            size="large"
            block
            onClick={handleUploadClick}
          >
            Escolher foto
          </UploadButton>
        </UploadArea>
      )}

      <FileInput
        ref={fileInputRef}
        type="file"
        onChange={handleFileChange}
        disabled={disabled}
      />
    </UploadContainer>
  );
}
