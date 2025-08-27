import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Plus, UserPlus, BookOpen, LogOut, User, GraduationCap } from 'lucide-react';
import api from '../services/api';

interface User {
  user_id: string;
  email: string;
  role: string;
  locale: string;
}

interface Child {
  student_id: string;
  grade_hint: string;
  relation: string;
}

interface Subject {
  code: string;
  title: string;
}

interface Stage {
  code: string;
  title: string;
}

const ParentDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [children, setChildren] = useState<Child[]>([]);
  const [subjects, setSubjects] = useState<Subject[]>([]);
  const [stages, setStages] = useState<Stage[]>([]);
  const [loading, setLoading] = useState(true);
  const [showAddChild, setShowAddChild] = useState(false);
  const [showEnroll, setShowEnroll] = useState(false);
  const [selectedChild, setSelectedChild] = useState<string>('');
  const [childForm, setChildForm] = useState({
    child_name: '',
    grade_hint: '',
    relation: 'child'
  });
  const [enrollmentForm, setEnrollmentForm] = useState({
    subject: '',
    stage: ''
  });

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const userInfo = JSON.parse(userData);
      if (userInfo.role === 'parent') {
        setUser(userInfo);
        loadChildren(userInfo.user_id);
        loadSubjects();
        loadStages();
      } else {
        navigate('/login');
      }
    } else {
      navigate('/login');
    }
    setLoading(false);
  }, [navigate]);

  const loadChildren = async (parentId: string) => {
    try {
      const response = await api.get(`/parent/children?parent_user_id=${parentId}`);
      setChildren(response.data.children || []);
    } catch (error) {
      console.error('Error loading children:', error);
    }
  };

  const loadSubjects = async () => {
    try {
      const response = await api.get('/modules');
      const modules = response.data.modules || [];
      const subjects = modules.map((m: any) => m.subject).filter(Boolean) as string[];
      const uniqueSubjects = Array.from(new Set(subjects)).map((subject: string) => ({
        code: subject.toLowerCase().replace(/\s+/g, ''),
        title: subject
      }));
      setSubjects(uniqueSubjects);
    } catch (error) {
      console.error('Error loading subjects:', error);
    }
  };

  const loadStages = async () => {
    try {
      // For now, we'll use hardcoded stages
      setStages([
        { code: 'stage_primary', title: 'Primary' },
        { code: 'stage_lower_secondary', title: 'Lower Secondary' },
        { code: 'stage_upper_secondary', title: 'Upper Secondary' },
        { code: 'stage_advanced', title: 'Advanced' }
      ]);
    } catch (error) {
      console.error('Error loading stages:', error);
    }
  };

  const handleLogout = async () => {
    try {
      await api.post('/logout');
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('user');
      navigate('/');
    }
  };

  const handleAddChild = async () => {
    if (!childForm.child_name) {
      alert('Please enter child\'s name');
      return;
    }

    try {
      const response = await api.post('/parent/add-child', {
        parent_user_id: user?.user_id,
        child_name: childForm.child_name,
        grade_hint: childForm.grade_hint,
        relation: childForm.relation
      });

      if (response.status === 201) {
        alert('Child added successfully!');
        setShowAddChild(false);
        setChildForm({ child_name: '', grade_hint: '', relation: 'child' });
        // Reload children list
        if (user) {
          loadChildren(user.user_id);
        }
      }
    } catch (error: any) {
      if (error.response?.data?.error) {
        alert(error.response.data.error);
      } else {
        alert('An error occurred while adding child');
      }
    }
  };

  const handleEnrollChild = async () => {
    if (!selectedChild || !enrollmentForm.subject || !enrollmentForm.stage) {
      alert('Please select all required fields');
      return;
    }

    try {
      const response = await api.post('/enrollment/enroll', {
        student_id: selectedChild,
        subject_code: enrollmentForm.subject,
        stage_code: enrollmentForm.stage
      });

      if (response.status === 201) {
        alert('Child enrolled successfully!');
        setShowEnroll(false);
        setSelectedChild('');
        setEnrollmentForm({ subject: '', stage: '' });
        // Reload children list to show updated info
        if (user) {
          loadChildren(user.user_id);
        }
      }
    } catch (error: any) {
      if (error.response?.data?.error) {
        alert(error.response.data.error);
      } else {
        alert('An error occurred during enrollment');
      }
    }
  };



  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600"></div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <GraduationCap className="h-8 w-8 text-indigo-600 mr-3" />
              <h1 className="text-xl font-semibold text-gray-900">
                Parent Dashboard
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-700">{user.email}</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                  Parent
                </span>
              </div>
              
              <button
                onClick={handleLogout}
                className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        <div className="px-4 py-6 sm:px-0">
          {/* Children Section */}
          <div className="bg-white rounded-lg shadow p-6 mb-6">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-lg font-medium text-gray-900">My Children</h2>
              <button
                onClick={() => setShowAddChild(true)}
                className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                <Plus className="h-4 w-4 mr-2" />
                Add Child
              </button>
            </div>

            {children.length === 0 ? (
              <div className="text-center py-8">
                <UserPlus className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No children added yet</h3>
                <p className="mt-1 text-sm text-gray-500">Add your child to start their learning journey</p>
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                {children.map((child) => (
                  <div key={child.student_id} className="border rounded-lg p-4">
                    <div className="flex items-center space-x-3">
                      <User className="h-8 w-8 text-gray-400" />
                      <div>
                        <h4 className="font-medium text-gray-900">Child #{child.student_id.slice(-4)}</h4>
                        <p className="text-sm text-gray-500">{child.grade_hint || 'Grade not specified'}</p>
                        <p className="text-xs text-gray-400">{child.relation}</p>
                      </div>
                    </div>
                    <button
                      onClick={() => {
                        setSelectedChild(child.student_id);
                        setShowEnroll(true);
                      }}
                      className="mt-3 w-full inline-flex items-center justify-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                    >
                      <BookOpen className="h-4 w-4 mr-2" />
                      Start Learning
                    </button>
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Quick Actions</h3>
              <div className="space-y-3">
                <button
                  onClick={() => navigate('/register/student')}
                  className="w-full inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                >
                  <UserPlus className="h-4 w-4 mr-2" />
                  Register New Child
                </button>
                <button
                  onClick={() => navigate('/')}
                  className="w-full inline-flex items-center justify-center px-4 py-2 border border-gray-300 text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <BookOpen className="h-4 w-4 mr-2" />
                  View Curriculum
                </button>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow p-6">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Learning Progress</h3>
              <div className="text-center py-8">
                <BookOpen className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No learning data yet</h3>
                <p className="mt-1 text-sm text-gray-500">Enroll your child in a subject to see progress</p>
              </div>
            </div>
          </div>
        </div>
      </main>

      {/* Add Child Modal */}
      {showAddChild && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Add New Child</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Child's Name
                  </label>
                  <input
                    type="text"
                    value={childForm.child_name}
                    onChange={(e) => setChildForm({...childForm, child_name: e.target.value})}
                    placeholder="Enter child's name"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Grade/Year
                  </label>
                  <input
                    type="text"
                    value={childForm.grade_hint}
                    onChange={(e) => setChildForm({...childForm, grade_hint: e.target.value})}
                    placeholder="e.g., Year 5, Grade 3"
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Relation
                  </label>
                  <select 
                    value={childForm.relation}
                    onChange={(e) => setChildForm({...childForm, relation: e.target.value})}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="child">Child</option>
                    <option value="son">Son</option>
                    <option value="daughter">Daughter</option>
                    <option value="ward">Ward</option>
                  </select>
                </div>
              </div>

              <div className="flex space-x-3 mt-6">
                <button
                  onClick={handleAddChild}
                  className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
                >
                  Add Child
                </button>
                <button
                  onClick={() => setShowAddChild(false)}
                  className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Enroll Child Modal */}
      {showEnroll && (
        <div className="fixed inset-0 bg-gray-600 bg-opacity-50 overflow-y-auto h-full w-full z-50">
          <div className="relative top-20 mx-auto p-5 border w-96 shadow-lg rounded-md bg-white">
            <div className="mt-3">
              <h3 className="text-lg font-medium text-gray-900 mb-4">Enroll Child in Learning</h3>
              
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Subject
                  </label>
                  <select
                    value={enrollmentForm.subject}
                    onChange={(e) => setEnrollmentForm({...enrollmentForm, subject: e.target.value})}
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                  >
                    <option value="">Select a subject</option>
                    {subjects.map((subject) => (
                      <option key={subject.code} value={subject.code}>
                        {subject.title}
                      </option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Stage
                  </label>
                  <select
                    value={enrollmentForm.stage}
                    onChange={(e) => setEnrollmentForm({...enrollmentForm, stage: e.target.value})}
                    className="w-full border border-gray-700 mb-2">
                    <option value="">Select a stage</option>
                    {stages.map((stage) => (
                      <option key={stage.code} value={stage.code}>
                        {stage.title}
                      </option>
                    ))}
                  </select>
                </div>
              </div>

              <div className="flex space-x-3 mt-6">
                <button
                  onClick={handleEnrollChild}
                  className="flex-1 bg-indigo-600 text-white px-4 py-2 rounded-md hover:bg-indigo-700"
                >
                  Enroll
                </button>
                <button
                  onClick={() => {
                    setShowEnroll(false);
                    setSelectedChild('');
                    setEnrollmentForm({ subject: '', stage: '' });
                  }}
                  className="flex-1 bg-gray-300 text-gray-700 px-4 py-2 rounded-md hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ParentDashboard;
