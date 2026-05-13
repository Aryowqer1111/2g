import random
from data.skills_config import COMMITTEE_INFO, FACTION_SKILL_BIASES

class CommitteeEngine:
    MAX_MEMBERS_PER_COMMITTEE = 5
    MAX_COMMISSIONS_PER_MEMBER = 2

    def __init__(self):
        self.available_committees = list(COMMITTEE_INFO.keys())
        self.members_assignments = {} 
        self.committee_members = {c: set() for c in self.available_committees}
        self.commission_heads = {} 

    def set_head(self, committee_name, member_id):
        if committee_name not in self.available_committees: return False
        if member_id == self.commission_heads.get(committee_name): return True
        if len(self.members_assignments.get(member_id, [])) >= 1: return False 
        if committee_name in self.commission_heads.values():
            old_head = [k for k,v in self.commission_heads.items() if v == member_id][0]
            del self.commission_heads[old_head]
        self.commission_heads[committee_name] = member_id
        if member_id not in self.committee_members[committee_name]:
            self.committee_members[committee_name].add(member_id)
            if member_id not in self.members_assignments: self.members_assignments[member_id] = []
        return True

    def get_committee_info(self, name):
        info = COMMITTEE_INFO.get(name, {})
        count = len(self.committee_members[name])
        head_id = self.commission_heads.get(name)
        return {**info, "current_count": count, "head_id": head_id, "max_count": self.MAX_MEMBERS_PER_COMMITTEE}

    def get_committee_load(self):
        return {c: len(members) for c, members in self.committee_members.items()}

    def assign_member_to_committee(self, member_id, committee_name):
        if committee_name not in self.available_committees: return False
        if len(self.committee_members[committee_name]) >= self.MAX_MEMBERS_PER_COMMITTEE: return False
        if member_id in self.members_assignments and len(self.members_assignments[member_id]) >= self.MAX_COMMISSIONS_PER_MEMBER: return False
        if committee_name in self.members_assignments.get(member_id, []): return False
        if member_id in self.commission_heads.values() and self.commission_heads[committee_name] != member_id: return False
        if member_id not in self.members_assignments: self.members_assignments[member_id] = []
        self.members_assignments[member_id].append(committee_name)
        self.committee_members[committee_name].add(member_id)
        return True

    def remove_member_from_committees(self, member_id):
        if member_id in self.members_assignments:
            for c in self.members_assignments[member_id]: self.committee_members[c].discard(member_id)
            del self.members_assignments[member_id]
        head_key = next((k for k,v in self.commission_heads.items() if v == member_id), None)
        if head_key: del self.commission_heads[head_key]

    def auto_fill_by_system(self, state):
        skills_engine = state.get("skills_engine")
        cc_df = state.get("cc_members")
        if not skills_engine or cc_df is None: return
        
        skills_map = {str(row["ID"]): skills_engine.competencies.get(row["ID"], {}) for _, row in cc_df.iterrows()}
        
        for comm_name, members_set in self.committee_members.items():
            current_count = len(members_set)
            if current_count >= 5: continue
            needed = 5 - current_count
            for _ in range(needed):
                best_id, best_score = None, -999
                for mid, sk in skills_map.items():
                    if mid in self.members_assignments and len(self.members_assignments[mid]) >= 2: continue
                    if mid in members_set: continue
                    score = sk.get("Хозяйственность", 5)
                    if "оборона" in comm_name.lower() or "безопас" in comm_name.lower(): score += sk.get("Военное дело", 0)*1.5
                    elif "идеол" in comm_name.lower(): score += sk.get("Интриги", 0)*1.5
                    elif "внешне" in comm_name.lower() or "диплом" in comm_name.lower(): score += sk.get("Дипломатия", 0)*1.5
                    if score + random.uniform(-1,1) > best_score: best_score = score; best_id = mid
                if best_id:
                    self.assign_member_to_committee(best_id, comm_name)
                    if best_score >= 7.0 and self.commission_heads.get(comm_name) is None: self.set_head(comm_name, best_id)

    def auto_fill_faction_balanced(self, state):
        faction_targets = {
            "ВПК": ["Комиссия по обороне и безопасности", "Комиссия по тяжёлой промышленности", "Комиссия по контролю за исполнением решений Пленума"],
            "Идеологи": ["Комиссия по идеологическим вопросам", "Комиссия по науке и образованию", "Государственная комиссия по делам религии и вероисповедания"],
            "Реформаторы": ["Комиссия по лёгкой и пищевой пром.", "Постоянная комиссия по сельскому хозяйству", "Комиссия по региональному развитию и союзным республикам"],
            "Регионы": ["Комиссия по региональному развитию и союзным республикам", "Постоянная комиссия по сельскому хозяйству", "Комиссия по лёгкой и пищевой пром."]
        }
        cc_df = state.get("cc_members")
        if cc_df is None: return
        
        for faction, targets in faction_targets.items():
            faction_ids = cc_df[cc_df["Фракция"]==faction]["ID"].astype(str).tolist()
            available = [mid for mid in faction_ids if mid not in self.members_assignments and len(self.members_assignments.get(mid,[]))<2]
            for comm in targets:
                if len(self.committee_members.get(comm, [])) >= 5: continue
                slots_to_fill = min(2, 5 - len(self.committee_members.get(comm, [])))
                for mid in available[:slots_to_fill]:
                    self.assign_member_to_committee(mid, comm)
                    if mid in available: available.remove(mid)
                    if len(self.members_assignments.get(mid,[])) >= 2: break
        self.auto_fill_by_system(state)