CREATE INDEX idx_user_role_user_id ON user_role(user_id);
CREATE INDEX idx_role_permission_role_id ON role_permission(role_id);
CREATE INDEX idx_permission_scope_permission_id ON permission_scope(permission_id);
CREATE INDEX idx_scope_name ON scope(name);