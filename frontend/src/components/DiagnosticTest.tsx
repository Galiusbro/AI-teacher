import React, { useState, useEffect } from 'react';
import { CheckCircle, Clock, Brain, Target, TrendingUp } from 'lucide-react';
import api from '../services/api';

interface Question {
  id: string;
  subject: string;
  difficulty_level: string;
  question_type: string;
  content: {
    question: string;
    options?: string[];
    correct_answer?: string;
  };
  target_age: number;
}

interface DiagnosticResult {
  is_correct: boolean;
  confidence_score: number;
  new_difficulty_level: string;
}

interface DiagnosticTestProps {
  studentId: string;
  age: number;
  subjects: string[];
  onComplete: (plan: any) => void;
  onClose: () => void;
}

const DiagnosticTest: React.FC<DiagnosticTestProps> = ({
  studentId,
  age,
  subjects,
  onComplete,
  onClose
}) => {
  const [currentQuestion, setCurrentQuestion] = useState<Question | null>(null);
  const [currentSubject, setCurrentSubject] = useState<string>('');
  const [currentSubjectIndex, setCurrentSubjectIndex] = useState(0);
  const [answer, setAnswer] = useState<string>('');
  const [timeSpent, setTimeSpent] = useState(0);
  const [isLoading, setIsLoading] = useState(false);
  const [isStarted, setIsStarted] = useState(false);
  const [results, setResults] = useState<DiagnosticResult[]>([]);
  const [showResult, setShowResult] = useState(false);
  const [lastResult, setLastResult] = useState<DiagnosticResult | null>(null);

  // Timer effect
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (currentQuestion && !showResult) {
      interval = setInterval(() => {
        setTimeSpent(prev => prev + 1);
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [currentQuestion, showResult]);

  const startDiagnostic = async () => {
    setIsLoading(true);
    try {
      await api.post('/diagnostic/start', {
        student_id: studentId,
        age: age,
        subjects: subjects
      });
      
      setIsStarted(true);
      setCurrentSubject(subjects[0]);
      await loadNextQuestion();
    } catch (error) {
      console.error('Error starting diagnostic:', error);
      alert('Ошибка при запуске диагностики');
    } finally {
      setIsLoading(false);
    }
  };

  const loadNextQuestion = async () => {
    if (currentSubjectIndex >= subjects.length) {
      // All subjects completed, get learning plan
      await completeDiagnostic();
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.post('/diagnostic/question', {
        student_id: studentId,
        subject: subjects[currentSubjectIndex]
      });

      if (response.data.question) {
        setCurrentQuestion(response.data.question);
        setCurrentSubject(response.data.question.subject);
        setAnswer('');
        setTimeSpent(0);
        setShowResult(false);
      } else {
        // No more questions for this subject, move to next
        setCurrentSubjectIndex(prev => prev + 1);
        if (currentSubjectIndex + 1 < subjects.length) {
          await loadNextQuestion();
        } else {
          await completeDiagnostic();
        }
      }
    } catch (error) {
      console.error('Error loading question:', error);
      alert('Ошибка при загрузке вопроса');
    } finally {
      setIsLoading(false);
    }
  };

  const submitAnswer = async () => {
    if (!currentQuestion || !answer.trim()) {
      alert('Пожалуйста, введите ответ');
      return;
    }

    setIsLoading(true);
    try {
      const response = await api.post('/diagnostic/answer', {
        student_id: studentId,
        question_id: currentQuestion.id,
        answer: answer,
        time_spent_sec: timeSpent
      });

      const result = response.data.result;
      setLastResult(result);
      setResults(prev => [...prev, result]);
      setShowResult(true);

      // Auto-advance after 3 seconds
      setTimeout(() => {
        setCurrentSubjectIndex(prev => prev + 1);
        loadNextQuestion();
      }, 3000);

    } catch (error) {
      console.error('Error submitting answer:', error);
      alert('Ошибка при отправке ответа');
    } finally {
      setIsLoading(false);
    }
  };

  const completeDiagnostic = async () => {
    setIsLoading(true);
    try {
      const response = await api.get(`/diagnostic/plan/${studentId}`);
      onComplete(response.data.plan);
    } catch (error) {
      console.error('Error getting learning plan:', error);
      alert('Ошибка при получении плана обучения');
    } finally {
      setIsLoading(false);
    }
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs.toString().padStart(2, '0')}`;
  };

  if (!isStarted) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg p-8 max-w-md w-full">
          <div className="text-center">
            <Brain className="mx-auto h-16 w-16 text-indigo-600 mb-4" />
            <h2 className="text-2xl font-bold text-gray-900 mb-4">
              Диагностика знаний
            </h2>
            <p className="text-gray-600 mb-6">
              Мы проведем тест для определения вашего уровня знаний по предметам:
            </p>
            <div className="space-y-2 mb-6">
              {subjects.map((subject, index) => (
                <div key={index} className="flex items-center justify-center">
                  <Target className="h-4 w-4 text-indigo-500 mr-2" />
                  <span className="text-gray-700">{subject}</span>
                </div>
              ))}
            </div>
            <div className="flex space-x-4">
              <button
                onClick={onClose}
                className="flex-1 px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
              >
                Отмена
              </button>
              <button
                onClick={startDiagnostic}
                disabled={isLoading}
                className="flex-1 px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
              >
                {isLoading ? 'Запуск...' : 'Начать тест'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (isLoading && !currentQuestion) {
    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
        <div className="bg-white rounded-lg p-8 max-w-md w-full text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-gray-600">Загрузка вопроса...</p>
        </div>
      </div>
    );
  }

  if (!currentQuestion) {
    return null;
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
      <div className="bg-white rounded-lg p-8 max-w-2xl w-full max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h3 className="text-lg font-semibold text-gray-900">
              {currentSubject}
            </h3>
            <p className="text-sm text-gray-500">
              Уровень: {currentQuestion.difficulty_level}
            </p>
          </div>
          <div className="flex items-center space-x-4">
            <div className="flex items-center text-sm text-gray-500">
              <Clock className="h-4 w-4 mr-1" />
              {formatTime(timeSpent)}
            </div>
            <div className="text-sm text-gray-500">
              Вопрос {results.length + 1}
            </div>
          </div>
        </div>

        {/* Question */}
        <div className="mb-6">
          <div className="bg-gray-50 rounded-lg p-6">
            <h4 className="text-lg font-medium text-gray-900 mb-4">
              {currentQuestion.content.question}
            </h4>
            
            {currentQuestion.question_type === 'dialogue' ? (
              <textarea
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Расскажите о своих интересах в этом предмете..."
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
                rows={4}
              />
            ) : currentQuestion.content.options ? (
              <div className="space-y-2">
                {currentQuestion.content.options.map((option, index) => (
                  <label key={index} className="flex items-center p-3 border border-gray-200 rounded-md hover:bg-gray-50 cursor-pointer">
                    <input
                      type="radio"
                      name="answer"
                      value={option}
                      checked={answer === option}
                      onChange={(e) => setAnswer(e.target.value)}
                      className="mr-3"
                    />
                    <span className="text-gray-700">{option}</span>
                  </label>
                ))}
              </div>
            ) : (
              <input
                type="text"
                value={answer}
                onChange={(e) => setAnswer(e.target.value)}
                placeholder="Введите ваш ответ..."
                className="w-full p-3 border border-gray-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
              />
            )}
          </div>
        </div>

        {/* Result Display */}
        {showResult && lastResult && (
          <div className="mb-6 p-4 rounded-lg bg-green-50 border border-green-200">
            <div className="flex items-center">
              <CheckCircle className="h-5 w-5 text-green-600 mr-2" />
              <span className="text-green-800 font-medium">
                {lastResult.is_correct ? 'Правильно!' : 'Неправильно'}
              </span>
            </div>
            <div className="mt-2 text-sm text-green-700">
              Уверенность: {Math.round(lastResult.confidence_score * 100)}% | 
              Новый уровень: {lastResult.new_difficulty_level}
            </div>
          </div>
        )}

        {/* Progress */}
        <div className="mb-6">
          <div className="flex justify-between text-sm text-gray-500 mb-2">
            <span>Прогресс</span>
            <span>{currentSubjectIndex + 1} из {subjects.length} предметов</span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div 
              className="bg-indigo-600 h-2 rounded-full transition-all duration-300"
              style={{ width: `${((currentSubjectIndex + 1) / subjects.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex justify-end space-x-4">
          <button
            onClick={onClose}
            className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
          >
            Прервать тест
          </button>
          {!showResult && (
            <button
              onClick={submitAnswer}
              disabled={!answer.trim() || isLoading}
              className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 disabled:opacity-50"
            >
              {isLoading ? 'Отправка...' : 'Ответить'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default DiagnosticTest;
