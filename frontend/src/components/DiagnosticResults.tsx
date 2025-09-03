import React from 'react';
import { Brain, Target, TrendingUp, BookOpen, Clock, Award, Lightbulb } from 'lucide-react';

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

interface DiagnosticResultsProps {
  plan: LearningPlan;
  onClose: () => void;
  onStartLearning: () => void;
}

const DiagnosticResults: React.FC<DiagnosticResultsProps> = ({
  plan,
  onClose,
  onStartLearning
}) => {
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

  const getCommunicationStyleIcon = (style: string) => {
    return style === 'expressive' ? '😊' : '😌';
  };

  const getTeachingApproachIcon = (approach: string) => {
    return approach === 'creative' ? '🎨' : '📋';
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-8 max-w-4xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <div className="flex justify-center mb-4">
            <div className="bg-indigo-100 rounded-full p-4">
              <Brain className="h-12 w-12 text-indigo-600" />
            </div>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 mb-2">
            Результаты диагностики
          </h2>
          <p className="text-gray-600">
            Ваш персональный план обучения готов!
          </p>
        </div>

        {/* Overall Level */}
        <div className="bg-gradient-to-r from-indigo-50 to-purple-50 rounded-lg p-6 mb-8">
          <div className="flex items-center justify-center mb-4">
            <span className="text-4xl mr-3">{getLevelIcon(plan.overall_level)}</span>
            <div>
              <h3 className="text-2xl font-bold text-gray-900">Общий уровень</h3>
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium ${getLevelColor(plan.overall_level)}`}>
                {plan.overall_level}
              </span>
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Subject Breakdown */}
          <div className="space-y-6">
            <h3 className="text-xl font-semibold text-gray-900 flex items-center">
              <BookOpen className="h-5 w-5 mr-2" />
              Результаты по предметам
            </h3>
            
            {Object.entries(plan.subject_breakdown).map(([subject, data]) => {
              const accuracy = data.questions_asked > 0 ? (data.correct_answers / data.questions_asked) * 100 : 0;
              
              return (
                <div key={subject} className="bg-white border border-gray-200 rounded-lg p-4">
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
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Вопросов:</span>
                      <span className="font-medium">{data.questions_asked}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-600">Время:</span>
                      <span className="font-medium">{Math.round(data.total_time_spent / 60)} мин</span>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* Psychological Profile & Recommendations */}
          <div className="space-y-6">
            {/* Psychological Profile */}
            <div>
              <h3 className="text-xl font-semibold text-gray-900 flex items-center mb-4">
                <Brain className="h-5 w-5 mr-2" />
                Психологический профиль
              </h3>
              
              <div className="bg-white border border-gray-200 rounded-lg p-4 mb-4">
                <div className="flex items-center mb-3">
                  <span className="text-2xl mr-2">{getCommunicationStyleIcon(plan.psychological_profile.communication_style)}</span>
                  <div>
                    <h4 className="font-medium text-gray-900">Стиль общения</h4>
                    <span className="text-sm text-gray-600 capitalize">
                      {plan.psychological_profile.communication_style}
                    </span>
                  </div>
                </div>
                
                {plan.psychological_profile.samples.length > 0 && (
                  <div>
                    <h5 className="text-sm font-medium text-gray-700 mb-2">Примеры ответов:</h5>
                    <div className="space-y-1">
                      {plan.psychological_profile.samples.map((sample, index) => (
                        <p key={index} className="text-sm text-gray-600 italic">
                          "{sample}"
                        </p>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Strengths & Weaknesses */}
            <div>
              <h3 className="text-xl font-semibold text-gray-900 flex items-center mb-4">
                <TrendingUp className="h-5 w-5 mr-2" />
                Сильные и слабые стороны
              </h3>
              
              {plan.strengths.length > 0 && (
                <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-4">
                  <h4 className="font-medium text-green-900 mb-2 flex items-center">
                    <Award className="h-4 w-4 mr-1" />
                    Сильные стороны
                  </h4>
                  <ul className="space-y-1">
                    {plan.strengths.map((strength, index) => (
                      <li key={index} className="text-sm text-green-800">• {strength}</li>
                    ))}
                  </ul>
                </div>
              )}
              
              {plan.weaknesses.length > 0 && (
                <div className="bg-orange-50 border border-orange-200 rounded-lg p-4">
                  <h4 className="font-medium text-orange-900 mb-2 flex items-center">
                    <Target className="h-4 w-4 mr-1" />
                    Области для развития
                  </h4>
                  <ul className="space-y-1">
                    {plan.weaknesses.map((weakness, index) => (
                      <li key={index} className="text-sm text-orange-800">• {weakness}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Recommendations */}
        <div className="mt-8 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-xl font-semibold text-gray-900 flex items-center mb-4">
            <Lightbulb className="h-5 w-5 mr-2" />
            Рекомендации по обучению
          </h3>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Подход к обучению</h4>
              <div className="flex items-center">
                <span className="text-2xl mr-2">{getTeachingApproachIcon(plan.recommendations.teaching_approach)}</span>
                <span className="text-sm text-gray-700 capitalize">
                  {plan.recommendations.teaching_approach}
                </span>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Время обучения</h4>
              <div className="flex items-center">
                <Clock className="h-4 w-4 mr-2 text-gray-500" />
                <span className="text-sm text-gray-700">
                  {plan.recommendations.study_schedule.daily_time} минут в день
                </span>
              </div>
            </div>
            
            <div>
              <h4 className="font-medium text-gray-900 mb-2">Приоритетные предметы</h4>
              <div className="text-sm text-gray-700">
                {plan.recommendations.immediate_focus.length > 0 
                  ? plan.recommendations.immediate_focus.join(', ')
                  : 'Все предметы'
                }
              </div>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-4 mt-8">
          <button
            onClick={onClose}
            className="px-6 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Закрыть
          </button>
          <button
            onClick={onStartLearning}
            className="px-6 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700"
          >
            Начать обучение
          </button>
        </div>
      </div>
    </div>
  );
};

export default DiagnosticResults;
