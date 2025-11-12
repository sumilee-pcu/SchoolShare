import React, { useState, useEffect } from 'react';
import './App.css';

const API_BASE_URL = 'https://schoolshare-api-production.up.railway.app';

const FACILITY_TYPES = {
  '': '전체',
  'stadium': '운동장',
  'gym': '체육관',
  'auditorium': '강당',
  'general': '일반교실',
  'special': '특별교실',
  'avr': '시청각실'
};

const AVAILABILITY_OPTIONS = {
  '': '전체',
  '개방': '개방',
  '미개방': '미개방',
  '정보없음': '정보없음'
};

function App() {
  const [facilities, setFacilities] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const [region, setRegion] = useState('노원구');
  const [facilityType, setFacilityType] = useState('');
  const [availability, setAvailability] = useState('');
  const [limit, setLimit] = useState(50);

  const fetchFacilities = async () => {
    setLoading(true);
    setError(null);

    try {
      const params = new URLSearchParams({
        region: region,
        limit: limit.toString()
      });

      if (facilityType) params.append('type', facilityType);
      if (availability) params.append('availability', availability);

      const response = await fetch(`${API_BASE_URL}/api/facilities?${params}`);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      setFacilities(data.items || []);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching facilities:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFacilities();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    fetchFacilities();
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>🏫 SchoolShare - 학교 시설 개방 정보</h1>
        <p>서울시 학교 시설의 개방 여부를 확인하세요</p>
      </header>

      <div className="search-container">
        <form onSubmit={handleSearch} className="search-form">
          <div className="form-group">
            <label>지역</label>
            <input
              type="text"
              value={region}
              onChange={(e) => setRegion(e.target.value)}
              placeholder="예: 노원구"
            />
          </div>

          <div className="form-group">
            <label>시설 유형</label>
            <select value={facilityType} onChange={(e) => setFacilityType(e.target.value)}>
              {Object.entries(FACILITY_TYPES).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>개방 여부</label>
            <select value={availability} onChange={(e) => setAvailability(e.target.value)}>
              {Object.entries(AVAILABILITY_OPTIONS).map(([key, label]) => (
                <option key={key} value={key}>{label}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>결과 개수</label>
            <input
              type="number"
              value={limit}
              onChange={(e) => setLimit(Math.min(200, Math.max(1, parseInt(e.target.value) || 50)))}
              min="1"
              max="200"
            />
          </div>

          <button type="submit" className="search-button" disabled={loading}>
            {loading ? '검색 중...' : '검색'}
          </button>
        </form>
      </div>

      {error && (
        <div className="error-message">
          ❌ 오류: {error}
        </div>
      )}

      {loading ? (
        <div className="loading">
          <div className="spinner"></div>
          <p>데이터를 불러오는 중...</p>
        </div>
      ) : (
        <div className="results-container">
          <div className="results-header">
            <h2>검색 결과</h2>
            <span className="results-count">{facilities.length}개의 시설</span>
          </div>

          {facilities.length === 0 ? (
            <div className="no-results">
              <p>검색 결과가 없습니다.</p>
              <p>다른 조건으로 검색해보세요.</p>
            </div>
          ) : (
            <div className="facilities-grid">
              {facilities.map((facility, index) => (
                <div key={index} className="facility-card">
                  <div className="facility-header">
                    <h3>{facility.school_name}</h3>
                    <span className={`availability-badge ${facility.availability === '개방' ? 'open' : facility.availability === '미개방' ? 'closed' : 'unknown'}`}>
                      {facility.availability}
                    </span>
                  </div>
                  <div className="facility-info">
                    <p className="facility-type">
                      <span className="icon">📍</span>
                      {facility.facility_type}
                    </p>
                    <p className="facility-address">
                      <span className="icon">📍</span>
                      {facility.address}
                    </p>
                    <p className="facility-updated">
                      <span className="icon">🕒</span>
                      업데이트: {new Date(facility.last_updated).toLocaleDateString('ko-KR')}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}

export default App;
