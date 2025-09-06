import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { api } from '../services/api';

interface File {
  id: number;
  original_name: string;
  current_name: string;
  upload_date: string;
  user_id: number;
  user_email: string;
}

const FileManagementPage: React.FC = () => {
  const { userId } = useParams<{ userId: string }>();
  const [files, setFiles] = useState<File[]>([]);
  const [editingFile, setEditingFile] = useState<number | null>(null);
  const [newFileName, setNewFileName] = useState('');

  useEffect(() => {
    loadFiles();
  }, [userId]);

  const loadFiles = async () => {
    try {
      const response = await api.admin.getUserFiles(Number(userId));
      setFiles(response);
    } catch (error) {
      console.error('Failed to load files:', error);
    }
  };

  const handleRename = async (fileId: number) => {
    try {
      await api.admin.renameFile(fileId, newFileName);
      setEditingFile(null);
      setNewFileName('');
      await loadFiles();
    } catch (error) {
      console.error('Failed to rename file:', error);
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">File Management</h1>
      <div className="bg-white shadow overflow-hidden sm:rounded-lg">
        <ul className="divide-y divide-gray-200">
          {files.map(file => (
            <li key={file.id} className="px-4 py-4 sm:px-6">
              <div className="flex items-center justify-between">
                <div className="flex-1 min-w-0">
                  {editingFile === file.id ? (
                    <div className="flex items-center space-x-2">
                      <input
                        type="text"
                        value={newFileName}
                        onChange={(e) => setNewFileName(e.target.value)}
                        className="form-input rounded-md shadow-sm w-full sm:w-96"
                        placeholder="New file name"
                      />
                      <button
                        onClick={() => handleRename(file.id)}
                        className="px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                      >
                        Save
                      </button>
                      <button
                        onClick={() => {
                          setEditingFile(null);
                          setNewFileName('');
                        }}
                        className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300"
                      >
                        Cancel
                      </button>
                    </div>
                  ) : (
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-primary-600">
                          {file.current_name}
                        </p>
                        <p className="text-sm text-gray-500">
                          Original: {file.original_name}
                        </p>
                        <p className="text-xs text-gray-400">
                          Uploaded: {new Date(file.upload_date).toLocaleDateString()}
                        </p>
                      </div>
                      <div className="flex items-center space-x-2">
                        <button
                          onClick={() => {
                            setEditingFile(file.id);
                            setNewFileName(file.current_name);
                          }}
                          className="px-3 py-1 bg-gray-100 text-gray-700 rounded hover:bg-gray-200"
                        >
                          Rename
                        </button>
                        <a
                          href={`/api/files/${file.id}/download`}
                          className="px-3 py-1 bg-primary-100 text-primary-700 rounded hover:bg-primary-200"
                          download
                        >
                          Download
                        </a>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default FileManagementPage;
