import React, { useState, useEffect } from 'react';
import { api } from '../services/api';

interface Ticket {
  id: number;
  title: string;
  description: string;
  status: 'open' | 'in_progress' | 'resolved';
  priority: 'low' | 'medium' | 'high';
  created_at: string;
  created_by: {
    email: string;
  };
  site_id: number;
}

interface NewTicket {
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
}

const TicketManagementPage: React.FC = () => {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [newTicket, setNewTicket] = useState<NewTicket>({
    title: '',
    description: '',
    priority: 'medium',
  });
  const [comment, setComment] = useState('');
  const [selectedTicket, setSelectedTicket] = useState<Ticket | null>(null);

  useEffect(() => {
    loadTickets();
  }, []);

  const loadTickets = async () => {
    try {
      const ticketList = await api.admin.tickets.list();
      setTickets(ticketList);
    } catch (error) {
      console.error('Failed to load tickets:', error);
    }
  };

  const handleCreateTicket = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await api.admin.tickets.create(newTicket);
      setNewTicket({ title: '', description: '', priority: 'medium' });
      await loadTickets();
    } catch (error) {
      console.error('Failed to create ticket:', error);
    }
  };

  const handleUpdateStatus = async (ticketId: number, newStatus: Ticket['status']) => {
    try {
      await api.admin.tickets.update(ticketId, { status: newStatus });
      await loadTickets();
    } catch (error) {
      console.error('Failed to update ticket status:', error);
    }
  };

  const handleAddComment = async (ticketId: number) => {
    if (!comment.trim()) return;
    try {
      await api.admin.tickets.addComment(ticketId, comment);
      setComment('');
      // Optionally reload ticket details here if you have an endpoint for that
    } catch (error) {
      console.error('Failed to add comment:', error);
    }
  };

  const getPriorityColor = (priority: Ticket['priority']) => {
    switch (priority) {
      case 'high':
        return 'text-red-600';
      case 'medium':
        return 'text-yellow-600';
      case 'low':
        return 'text-green-600';
      default:
        return '';
    }
  };

  const getStatusBadgeColor = (status: Ticket['status']) => {
    switch (status) {
      case 'open':
        return 'bg-blue-100 text-blue-800';
      case 'in_progress':
        return 'bg-yellow-100 text-yellow-800';
      case 'resolved':
        return 'bg-green-100 text-green-800';
      default:
        return '';
    }
  };

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold mb-6">Ticket Management</h1>

      {/* Create Ticket Form */}
      <div className="bg-white rounded-lg shadow-md p-6 mb-6">
        <h2 className="text-xl font-semibold mb-4">Create New Ticket</h2>
        <form onSubmit={handleCreateTicket} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Title</label>
            <input
              type="text"
              value={newTicket.title}
              onChange={(e) => setNewTicket({ ...newTicket, title: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Description</label>
            <textarea
              value={newTicket.description}
              onChange={(e) => setNewTicket({ ...newTicket, description: e.target.value })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
              rows={3}
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">Priority</label>
            <select
              value={newTicket.priority}
              onChange={(e) => setNewTicket({ ...newTicket, priority: e.target.value as NewTicket['priority'] })}
              className="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
            </select>
          </div>
          <button
            type="submit"
            className="bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2"
          >
            Create Ticket
          </button>
        </form>
      </div>

      {/* Ticket List */}
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-semibold mb-4">Tickets</h2>
        <div className="space-y-4">
          {tickets.map((ticket) => (
            <div key={ticket.id} className="border rounded-lg p-4">
              <div className="flex justify-between items-start mb-2">
                <div>
                  <h3 className="text-lg font-medium">{ticket.title}</h3>
                  <p className="text-sm text-gray-500">
                    Created by {ticket.created_by.email} on{' '}
                    {new Date(ticket.created_at).toLocaleDateString()}
                  </p>
                </div>
                <span className={`${getPriorityColor(ticket.priority)} text-sm font-medium`}>
                  {ticket.priority.toUpperCase()}
                </span>
              </div>
              <p className="text-gray-700 mb-4">{ticket.description}</p>
              <div className="flex items-center justify-between">
                <div className="flex space-x-2">
                  <select
                    value={ticket.status}
                    onChange={(e) => handleUpdateStatus(ticket.id, e.target.value as Ticket['status'])}
                    className="rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  >
                    <option value="open">Open</option>
                    <option value="in_progress">In Progress</option>
                    <option value="resolved">Resolved</option>
                  </select>
                </div>
                <span className={`${getStatusBadgeColor(ticket.status)} px-2 py-1 rounded-full text-sm`}>
                  {ticket.status.replace('_', ' ').toUpperCase()}
                </span>
              </div>
              <div className="mt-4">
                <textarea
                  placeholder="Add a comment..."
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  className="w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500"
                  rows={2}
                />
                <button
                  onClick={() => handleAddComment(ticket.id)}
                  className="mt-2 bg-gray-100 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2"
                >
                  Add Comment
                </button>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default TicketManagementPage;
