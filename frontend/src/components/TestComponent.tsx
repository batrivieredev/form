import React from 'react';

const TestComponent: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8">
        <div className="bg-white rounded-lg shadow-xl p-6">
          <h1 className="text-4xl font-bold text-primary-600 mb-4">
            TailwindCSS Test
          </h1>
          <p className="text-secondary-700 mb-4">
            This component tests various Tailwind utilities:
          </p>
          <div className="space-y-4">
            <button className="bg-primary-500 hover:bg-primary-600 text-white font-semibold py-2 px-4 rounded-lg transition duration-150 ease-in-out">
              Primary Button
            </button>
            <div className="border border-secondary-200 rounded-lg p-4">
              <input
                type="text"
                placeholder="Form input test"
                className="form-input w-full rounded-md border-secondary-300 shadow-sm focus:border-primary-500 focus:ring-primary-500"
              />
            </div>
            <div className="bg-secondary-50 p-4 rounded-4xl">
              <p className="text-secondary-800">Custom border radius test</p>
            </div>
            <div className="w-128 bg-primary-100 p-4 rounded-lg">
              <p className="text-primary-800">Custom spacing test (w-128)</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TestComponent;
