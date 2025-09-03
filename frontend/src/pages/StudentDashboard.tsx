import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { LogOut, User, BookOpen, Brain, Play, BarChart3, Target, Clock } from 'lucide-react';
import api from '../services/api';
import DiagnosticTest from '../components/DiagnosticTest';
import DiagnosticResults from '../components/DiagnosticResults';

interface User {
  user_id: string;
  email: string;
  role: string;
  locale: string;
}

interface LearningPlan {
  overall_level: string;
  subject_breakdown: {
    [subject: string]: {
      current_level: string;
      questions_asked: number;
      correct_answers: number;
      total_time_spent: number;
    };
  };
  strengths: string[];
  weaknesses: string[];
  psychological_profile: {
    communication_style: string;
    samples: string[];
  };
  recommendations: {
    immediate_focus: string[];
    study_schedule: {
      daily_time: number;
      preferred_subjects: string[];
    };
    teaching_approach: string;
  };
}

const StudentDashboard: React.FC = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);
  const [showDiagnostic, setShowDiagnostic] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [learningPlan, setLearningPlan] = useState<LearningPlan | null>(null);
  const [hasCompletedDiagnostic, setHasCompletedDiagnostic] = useState(false);

  useEffect(() => {
    const userData = localStorage.getItem('user');
    if (userData) {
      const userInfo = JSON.parse(userData);
      if (userInfo.role === 'student') {
        setUser(userInfo);
        // Check if student has completed diagnostic
        checkDiagnosticStatus(userInfo.user_id);
      } else {
        navigate('/login');
      }
    } else {
      navigate('/login');
    }
    setLoading(false);
  }, [navigate]);

  const checkDiagnosticStatus = async (studentId: string) => {
    try {
      // Try to get learning plan - if it exists, diagnostic was completed
      const response = await api.get(`/diagnostic/plan/${studentId}`);
      if (response.data.plan) {
        setLearningPlan(response.data.plan);
        setHasCompletedDiagnostic(true);
      }
    } catch (error) {
      // No learning plan found, diagnostic not completed
      setHasCompletedDiagnostic(false);
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

  const handleDiagnosticComplete = (plan: LearningPlan) => {
    setLearningPlan(plan);
    setShowDiagnostic(false);
    setShowResults(true);
    setHasCompletedDiagnostic(true);
  };

  const handleStartLearning = () => {
    setShowResults(false);
    // Navigate to learning interface or show learning modules
    alert('Переход к обучению будет реализован в следующих версиях');
  };

  const getLevelColor = (level: string) => {
    const colors: { [key: string]: string } = {
      'beginner': 'bg-blue-100 text-blue-800',
      'elementary': 'bg-green-100 text-green-800',
      'intermediate': 'bg-yellow-100 text-yellow-800',
      'advanced': 'bg-orange-100 text-orange-800',
      'expert': 'bg-red-100 text-red-800'
    };
    return colors[level] || 'bg-gray-100 text-gray-800';
  };

  const getLevelIcon = (level: string) => {
    const icons: { [key: string]: string } = {
      'beginner': '🌱',
      'elementary': '📚',
      'intermediate': '🎯',
      'advanced': '🏆',
      'expert': '👑'
    };
    return icons[level] || '📖';
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
              <BookOpen className="h-8 w-8 text-indigo-600 mr-3" />
              <h1 className="text-xl font-semibold text-gray-900">
                Ayaal Student Dashboard
              </h1>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-2">
                <User className="h-5 w-5 text-gray-400" />
                <span className="text-sm text-gray-700">{user.email}</span>
                <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-indigo-100 text-indigo-800">
                  {user.role}
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
          {!hasCompletedDiagnostic ? (
            /* Diagnostic Not Completed */
            <div className="text-center">
              <div className="bg-white rounded-lg shadow-sm border p-8">
                <div className="flex justify-center mb-6">
                  <div className="bg-indigo-100 rounded-full p-6">
                    <Brain className="h-16 w-16 text-indigo-600" />
                  </div>
                </div>
                
                <h2 className="text-3xl font-bold text-gray-900 mb-4">
                  Добро пожаловать в Ayaal!
                </h2>
                
                <p className="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
                  Для создания вашего персонального плана обучения нам нужно провести диагностику ваших знаний. 
                  Это займет всего несколько минут и поможет нам подобрать оптимальную программу обучения.
                </p>
                
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-6 mb-8 max-w-2xl mx-auto">
                  <h3 className="text-lg font-semibold text-blue-900 mb-3">
                    Что включает диагностика:
                  </h3>
                  <ul className="text-left text-blue-800 space-y-2">
                    <li className="flex items-center">
                      <Target className="h-4 w-4 mr-2" />
                      Тестирование по основным предметам
                    </li>
                    <li className="flex items-center">
                      <Brain className="h-4 w-4 mr-2" />
                      Анализ стиля обучения
                    </li>
                    <li className="flex items-center">
                      <BarChart3 className="h-4 w-4 mr-2" />
                      Определение уровня знаний
                    </li>
                    <li className="flex items-center">
                      <Clock className="h-4 w-4 mr-2" />
                      Создание персонального плана
                    </li>
                  </ul>
                </div>
                
                <button
                  onClick={() => setShowDiagnostic(true)}
                  className="inline-flex items-center px-8 py-3 border border-transparent text-lg font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  <Play className="h-5 w-5 mr-2" />
                  Начать диагностику
                </button>
              </div>
            </div>
          ) : (
            /* Diagnostic Completed - Show Learning Plan */
            <div className="space-y-6">
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <div className="flex items-center justify-between mb-6">
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900">
                      Ваш план обучения
                    </h2>
                    <p className="text-gray-600">
                      Персональная программа на основе результатов диагностики
                    </p>
                  </div>
                  <button
                    onClick={() => setShowDiagnostic(true)}
                    className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                  >
                    <Brain className="h-4 w-4 mr-2" />
                    Повторить диагностику
                  </button>
                </div>
                
                {learningPlan && (
                  <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    {/* Overall Level */}
                    <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6">
                      <div className="text-center">
                        <span className="text-4xl mb-2 block">{getLevelIcon(learningPlan.overall_level)}</span>
                        <h3 className="text-lg font-semibold text-gray-900 mb-2">Общий уровень</h3>
                        <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getLevelColor(learningPlan.overall_level)}`}>
                          {learningPlan.overall_level}
                        </span>
                      </div>
                    </div>
                    
                    {/* Study Schedule */}
                    <div className="bg-green-50 rounded-lg p-6">
                      <div className="flex items-center mb-3">
                        <Clock className="h-5 w-5 text-green-600 mr-2" />
                        <h3 className="text-lg font-semibold text-gray-900">Расписание</h3>
                      </div>
                      <p className="text-green-800">
                        {learningPlan.recommendations.study_schedule.daily_time} минут в день
                      </p>
                      <p className="text-sm text-green-600 mt-1">
                        Подход: {learningPlan.recommendations.teaching_approach}
                      </p>
                    </div>
                    
                    {/* Focus Areas */}
                    <div className="bg-orange-50 rounded-lg p-6">
                      <div className="flex items-center mb-3">
                        <Target className="h-5 w-5 text-orange-600 mr-2" />
                        <h3 className="text-lg font-semibold text-gray-900">Фокус</h3>
                      </div>
                      <p className="text-orange-800">
                        {learningPlan.recommendations.immediate_focus.length > 0 
                          ? learningPlan.recommendations.immediate_focus.join(', ')
                          : 'Все предметы'
                        }
                      </p>
                    </div>
                  </div>
                )}
              </div>
              
              {/* Subject Progress */}
              {learningPlan && (
                <div className="bg-white rounded-lg shadow-sm border p-6">
                  <h3 className="text-xl font-semibold text-gray-900 mb-4">
                    Прогресс по предметам
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {Object.entries(learningPlan.subject_breakdown).map(([subject, data]) => {
                      const accuracy = data.questions_asked > 0 ? (data.correct_answers / data.questions_asked) * 100 : 0;
                      
                      return (
                        <div key={subject} className="border border-gray-200 rounded-lg p-4">
                          <div className="flex justify-between items-start mb-3">
                            <h4 className="font-medium text-gray-900">{subject}</h4>
                            <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getLevelColor(data.current_level)}`}>
                              {getLevelIcon(data.current_level)} {data.current_level}
                            </span>
                          </div>
                          <div className="space-y-2">
                            <div className="flex justify-between text-sm">
                              <span className="text-gray-600">Точность:</span>
                              <span className="font-medium">{Math.round(accuracy)}%</span>
                            </div>
                            <div className="w-full bg-gray-200 rounded-full h-2">
                              <div 
                                className="bg-indigo-600 h-2 rounded-full"
                                style={{ width: `${accuracy}%` }}
                              ></div>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              )}
              
              {/* Learning Actions */}
              <div className="bg-white rounded-lg shadow-sm border p-6">
                <h3 className="text-xl font-semibold text-gray-900 mb-4">
                  Начать обучение
                </h3>
                <p className="text-gray-600 mb-6">
                  Ваш персональный план готов! Начните обучение с рекомендованных модулей.
                </p>
                <button
                  onClick={handleStartLearning}
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md text-white bg-indigo-600 hover:bg-indigo-700"
                >
                  <Play className="h-5 w-5 mr-2" />
                  Начать обучение
                </button>
              </div>
            </div>
          )}
        </div>
      </main>

      {/* Diagnostic Test Modal */}
      {showDiagnostic && (
        <DiagnosticTest
          studentId={user.user_id}
          age={12} // This should come from user profile
          subjects={['Mathematics', 'English', 'Science']}
          onComplete={handleDiagnosticComplete}
          onClose={() => setShowDiagnostic(false)}
        />
      )}

      {/* Diagnostic Results Modal */}
      {showResults && learningPlan && (
        <DiagnosticResults
          plan={learningPlan}
          onClose={() => setShowResults(false)}
          onStartLearning={handleStartLearning}
        />
      )}
    </div>
  );
};

export default StudentDashboard;
