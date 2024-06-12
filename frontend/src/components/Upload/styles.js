import styled from "styled-components";
import { motion } from "framer-motion";
import { Button } from "antd";

export const UploadContainer = styled(motion.div)`
  display: flex;
  flex-direction: column;
  max-width: 500px;
  width: 94vw;
  gap: 16px;
`;

export const Image = styled(motion.img)`
  width: 100%;
  height: 100%;
  object-fit: cover;

  transition: bottom 0.5s ease-in-out;

  ${(props) =>
    props.disabled &&
    `
    filter: grayscale(100%);
    opacity: 0.6;
  `}
`;

export const ImageContainer = styled(motion.div)`
  position: relative;
  width: 100%;
  height: 400px;
  border-radius: 10px;
  border: 1px solid ${(props) => props.theme.colors.gray[100]};
  overflow: hidden;
  cursor: pointer;

  transition: bottom 0.5s ease-in-out;

  ${(props) =>
    props.disabled &&
    `
    cursor: not-allowed;
    opacity: 0.6;
  `}
`;

export const UploadArea = styled(motion.div)`
  display: flex;
  flex-direction: column;
  gap: 8px;
  width: 100%;
  height: 200px;
  border-radius: 10px;
  border: 1px dashed ${(props) => props.theme.colors.gray[300]};

  align-items: center;
  justify-content: space-between;
  padding: 16px;

  transition: all 0.3s ease;
  cursor: pointer;

  ${(props) =>
    props.$isFileHovering &&
    `
    border: 1px dashed ${props.theme.colors.blue[500]};
  `}

  ${(props) =>
    props.disabled &&
    `
    cursor: not-allowed;
    opacity: 0.6;
    color: ${props.theme.colors.gray[300]};
    background-color: ${props.theme.colors.gray[50]};
  `}
`;

export const FileInput = styled.input`
  display: none;
`;

export const UploadButton = styled(Button)`
  ${(props) =>
    props.disabled &&
    `
    cursor: not-allowed;
    opacity: 0.6;
  `}
`;

export const DeleteButton = styled.button`
  border: none;
  background-color: ${(props) => props.theme.colors.red[50]};
  color: ${(props) => props.theme.colors.red[600]};
  cursor: pointer;
  height: 32px;
  width: 32px;
  position: absolute;
  top: 8px;
  right: 8px;
  border-radius: 50%;
  z-index: 100;

  outline: none;

  transition: bottom 0.5s ease-in-out;

  &:hover {
    color: ${(props) => props.theme.colors.red[800]};
  }

  &:focus {
    color: ${(props) => props.theme.colors.red[800]};
    background-color: ${(props) => props.theme.colors.red[50]};
  }

  ${(props) =>
    props.disabled &&
    `
    cursor: not-allowed;
    opacity: 0.6;
  `}
`;

export const LoadingIndicator = styled.div`
  margin-top: 10px;
`;
