import axios from 'axios';
import axiosInstance from '../config/axios';

interface LoginCredentials {
  email: string;
  password: string;
}

interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface User {
  id: number;
  email: string;
  username: string;
  role: string;
  created_at: string;
  last_login?: string;
  site_id?: number;
  is_active: boolean;
}

interface Form {
  id: number;
  title: string;
  description: string;
  status: 'active' | 'inactive';
  created_at: string;
  response_count: number;
}

interface Message {
  id: number;
  sender_id: number;
  sender_email: string;
  content: string;
  created_at: string;
  read: boolean;
}

interface File {
  id: number;
  original_name: string;
  current_name: string;
  upload_date: string;
  user_id: number;
  user_email: string;
}

interface Ticket {
  id: number;
  title: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  created_by: User;
  site_id: number;
}

export const api = {
  auth: {
    login: async (credentials: LoginCredentials): Promise<LoginResponse> => {
      const response = await axiosInstance.post<LoginResponse>('/auth/login', {
        username: credentials.email,  // FastAPI OAuth2 uses 'username' field
        password: credentials.password,
      });
      return response.data;
    },
    getProfile: async (): Promise<User> => {
      const response = await axiosInstance.get<User>('/auth/profile');
      return response.data;
    },
  },

  forms: {
    list: async (): Promise<Form[]> => {
      const response = await axiosInstance.get<Form[]>('/forms');
      return response.data;
    },
    get: async (id: number): Promise<Form> => {
      const response = await axiosInstance.get<Form>(`/forms/${id}`);
      return response.data;
    },
    create: async (data: Partial<Form>): Promise<Form> => {
      const response = await axiosInstance.post<Form>('/forms', data);
      return response.data;
    },
    update: async (id: number, data: Partial<Form>): Promise<Form> => {
      const response = await axiosInstance.put<Form>(`/forms/${id}`, data);
      return response.data;
    },
    delete: async (id: number): Promise<void> => {
      await axiosInstance.delete(`/forms/${id}`);
    },
    exportPDF: async (id: number): Promise<Blob> => {
      const { data } = await axios.get<Blob>(`${axiosInstance.defaults.baseURL}/forms/${id}/export-pdf`, {
        responseType: 'blob',
        headers: axiosInstance.defaults.headers,
      });
      return data;
    },
  },

  messages: {
    list: async (): Promise<Message[]> => {
      const response = await axiosInstance.get<Message[]>('/messages');
      return response.data;
    },
    get: async (id: number): Promise<Message> => {
      const response = await axiosInstance.get<Message>(`/messages/${id}`);
      return response.data;
    },
    send: async (content: string): Promise<Message> => {
      const response = await axiosInstance.post<Message>('/messages', { content });
      return response.data;
    },
    markAsRead: async (id: number): Promise<void> => {
      await axiosInstance.put(`/messages/${id}/read`);
    },
  },

  admin: {
    // User management
    listUsers: async (): Promise<User[]> => {
      const response = await axiosInstance.get<User[]>('/admin/users');
      return response.data;
    },
    createUser: async (userData: Partial<User>): Promise<User> => {
      const response = await axiosInstance.post<User>('/admin/users', userData);
      return response.data;
    },
    updateUser: async (id: number, userData: Partial<User>): Promise<User> => {
      const response = await axiosInstance.put<User>(`/admin/users/${id}`, userData);
      return response.data;
    },
    deleteUser: async (id: number): Promise<void> => {
      await axiosInstance.delete(`/admin/users/${id}`);
    },

    // File management
    getUserFiles: async (userId: number): Promise<File[]> => {
      const response = await axiosInstance.get<File[]>(`/admin/users/${userId}/files`);
      return response.data;
    },
    renameFile: async (fileId: number, newName: string): Promise<File> => {
      const response = await axiosInstance.put<File>(`/admin/files/${fileId}/rename`, {
        new_name: newName,
      });
      return response.data;
    },
    downloadFile: async (fileId: number): Promise<Blob> => {
      const { data } = await axios.get<Blob>(`${axiosInstance.defaults.baseURL}/admin/files/${fileId}/download`, {
        responseType: 'blob',
        headers: axiosInstance.defaults.headers,
      });
      return data;
    },

    // Site management
    createSite: async (siteData: { name: string, admin_email: string }): Promise<void> => {
      await axiosInstance.post('/admin/sites', siteData);
    },
    updateSite: async (siteId: number, siteData: { name?: string, admin_email?: string }): Promise<void> => {
      await axiosInstance.put(`/admin/sites/${siteId}`, siteData);
    },
    deleteSite: async (siteId: number): Promise<void> => {
      await axiosInstance.delete(`/admin/sites/${siteId}`);
    },

    // Ticket system
    tickets: {
      list: async (): Promise<Ticket[]> => {
        const response = await axiosInstance.get<Ticket[]>('/admin/tickets');
        return response.data;
      },
      create: async (data: { title: string, description: string, priority: Ticket['priority'] }): Promise<Ticket> => {
        const response = await axiosInstance.post<Ticket>('/admin/tickets', data);
        return response.data;
      },
      update: async (id: number, data: { status: Ticket['status'] }): Promise<Ticket> => {
        const response = await axiosInstance.put<Ticket>(`/admin/tickets/${id}`, data);
        return response.data;
      },
      addComment: async (ticketId: number, comment: string): Promise<void> => {
        await axiosInstance.post(`/admin/tickets/${ticketId}/comments`, { content: comment });
      },
    },
  },
};
